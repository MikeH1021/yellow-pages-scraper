#!/usr/bin/env python3
"""
yp-cli.py - Command-line interface for the Yellow Pages Scraper API.

Designed for programmatic use by AI agents (Claude Code) and humans alike.
Requires: requests (pip install requests)

Usage:
    yp-cli.py login --user mike --password changeme123
    yp-cli.py scrape --keywords "plumbers,electricians" --locations "Miami FL"
    yp-cli.py status
    yp-cli.py results
    yp-cli.py download
    yp-cli.py suggest --icp "roofing companies in the southeast"
"""

import argparse
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

CONFIG_DIR = os.path.expanduser("~/.yp-scraper")
SESSION_FILE = os.path.join(CONFIG_DIR, "session")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config")

DEFAULT_BASE_URL = "https://scrape-yp.mikehernandez.co"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_config_dir():
    os.makedirs(CONFIG_DIR, mode=0o700, exist_ok=True)


def _load_config():
    """Load saved config (base_url, etc.)."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def _save_config(cfg):
    _ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
    os.chmod(CONFIG_FILE, 0o600)


def _get_base_url(args):
    """Resolve base URL: CLI flag > saved config > default."""
    if getattr(args, "url", None):
        return args.url.rstrip("/")
    cfg = _load_config()
    return cfg.get("base_url", DEFAULT_BASE_URL).rstrip("/")


def _save_session(cookies_dict, base_url):
    _ensure_config_dir()
    data = {"cookies": cookies_dict, "base_url": base_url}
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)
    os.chmod(SESSION_FILE, 0o600)


def _load_session():
    """Return (cookies_dict, base_url) or (None, None)."""
    if not os.path.exists(SESSION_FILE):
        return None, None
    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
        return data.get("cookies", {}), data.get("base_url")
    except (json.JSONDecodeError, IOError):
        return None, None


def _get_session(args):
    """Build a requests.Session with saved auth cookies. Exits on failure."""
    cookies, saved_url = _load_session()
    if not cookies:
        _die("Not logged in. Run: yp-cli.py login --user <user> --password <pass>")
    base_url = _get_base_url(args)
    s = requests.Session()
    s.cookies.update(cookies)
    return s, base_url


def _die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def _output(data, as_json=False):
    """Print output - JSON or human-readable."""
    if as_json:
        print(json.dumps(data, indent=2))
    else:
        if isinstance(data, dict):
            for k, v in data.items():
                print(f"{k}: {v}")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for k, v in item.items():
                        print(f"  {k}: {v}")
                    print()
                else:
                    print(f"  {item}")
        else:
            print(data)


def _check_response(resp, context="request"):
    """Check HTTP response, exit with error message on failure."""
    if resp.status_code == 401 or resp.status_code == 302:
        _die("Session expired or invalid. Run: yp-cli.py login --user <user> --password <pass>")
    if resp.status_code >= 400:
        try:
            body = resp.json()
            msg = body.get("error", resp.text[:200])
        except Exception:
            msg = resp.text[:200]
        _die(f"{context} failed (HTTP {resp.status_code}): {msg}")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_login(args):
    """Authenticate and save session cookie."""
    base_url = _get_base_url(args)

    if not args.user or not args.password:
        _die("--user and --password are required for login")

    s = requests.Session()
    # POST login form
    resp = s.post(
        f"{base_url}/login",
        data={"username": args.user, "password": args.password},
        allow_redirects=False,
    )

    # Successful login returns a 302 redirect to /dashboard
    if resp.status_code not in (200, 302):
        _die(f"Login failed (HTTP {resp.status_code})")

    # Check we actually got a session cookie
    if not s.cookies.get_dict():
        # Try following redirect and check
        resp2 = s.get(f"{base_url}/dashboard", allow_redirects=False)
        if resp2.status_code == 302 or not s.cookies.get_dict():
            _die("Login failed: invalid credentials")

    cookies = s.cookies.get_dict()
    _save_session(cookies, base_url)

    # Optionally save URL to config
    if args.url:
        cfg = _load_config()
        cfg["base_url"] = base_url
        _save_config(cfg)

    result = {"status": "ok", "message": f"Logged in as {args.user}", "base_url": base_url}
    _output(result, args.json)


def cmd_scrape(args):
    """Start a scraping job."""
    s, base_url = _get_session(args)

    if not args.keywords:
        _die("--keywords is required")
    if not args.locations:
        _die("--locations is required")

    payload = {
        "keywords": args.keywords,
        "locations": args.locations,
        "max_pages": args.pages,
        "concurrent": args.concurrent,
        "use_proxies": args.proxies,
    }

    resp = s.post(f"{base_url}/api/start-scrape", json=payload, allow_redirects=False)
    _check_response(resp, "Start scrape")

    data = resp.json()
    if not data.get("success"):
        _die(data.get("error", "Unknown error starting scrape"))

    job_id = data.get("job_id")
    total = data.get("total_searches", 0)

    if not args.wait:
        result = {
            "status": "submitted",
            "job_id": job_id,
            "total_searches": total,
            "message": data.get("message", ""),
        }
        _output(result, args.json)
        return

    # --wait mode: poll until complete
    print(f"Job {job_id} submitted ({total} searches). Waiting for completion...", file=sys.stderr)

    while True:
        time.sleep(3)
        resp = s.get(f"{base_url}/api/progress", params={"job_id": job_id}, allow_redirects=False)
        _check_response(resp, "Progress check")
        pdata = resp.json()

        progress = pdata.get("progress", {})
        completed = progress.get("completed", 0)
        total_s = progress.get("total_searches", total)
        found = progress.get("businesses_found", 0)
        errors = progress.get("errors", 0)
        status = pdata.get("status", "unknown")

        pct = int((completed / total_s * 100) if total_s > 0 else 0)
        print(
            f"  [{pct:3d}%] {completed}/{total_s} searches | {found} businesses | {errors} errors | status={status}",
            file=sys.stderr,
        )

        if not pdata.get("running", False):
            break

    # Re-fetch final state (output_files may not be set until after status changes)
    time.sleep(1)
    final_resp = s.get(f"{base_url}/api/progress", params={"job_id": job_id})
    if final_resp.ok:
        pdata = final_resp.json()
        status = pdata.get("status", status)
        found = pdata.get("progress", {}).get("businesses_found", found)
    output_files = pdata.get("output_files", [])
    result = {
        "status": status,
        "job_id": job_id,
        "total_searches": total_s,
        "completed": completed,
        "businesses_found": found,
        "errors": errors,
        "output_files": output_files,
    }

    # Auto-download the latest result
    if output_files and status in ("complete", "completed", "done", "stopped", "error"):
        latest = output_files[0]
        out_path = args.output if args.output else latest
        print(f"Downloading {latest} -> {out_path}", file=sys.stderr)
        dl_resp = s.get(f"{base_url}/api/download", params={"file": latest}, allow_redirects=False)
        if dl_resp.status_code == 200:
            with open(out_path, "wb") as f:
                f.write(dl_resp.content)
            result["downloaded"] = out_path
            result["download_size"] = len(dl_resp.content)
        else:
            result["download_error"] = f"HTTP {dl_resp.status_code}"

    _output(result, args.json)


def cmd_status(args):
    """Check job progress."""
    s, base_url = _get_session(args)

    params = {}
    if args.job_id:
        params["job_id"] = args.job_id

    resp = s.get(f"{base_url}/api/progress", params=params, allow_redirects=False)
    _check_response(resp, "Status check")

    data = resp.json()
    progress = data.get("progress", {})
    result = {
        "job_id": data.get("job_id", "none"),
        "status": data.get("status", "no_job"),
        "running": data.get("running", False),
        "total_searches": progress.get("total_searches", 0),
        "completed": progress.get("completed", 0),
        "businesses_found": progress.get("businesses_found", 0),
        "errors": progress.get("errors", 0),
        "output_files": data.get("output_files", []),
    }
    _output(result, args.json)


def cmd_results(args):
    """List available result files."""
    s, base_url = _get_session(args)

    resp = s.get(f"{base_url}/api/list-results", allow_redirects=False)
    _check_response(resp, "List results")

    data = resp.json()
    files = data.get("files", [])

    if args.json:
        print(json.dumps(files, indent=2))
        return

    if not files:
        print("No result files available.")
        return

    print(f"{'FILENAME':<50} {'ROWS':>8} {'SIZE':>10} {'CREATED'}")
    print("-" * 90)
    for f in files:
        size_kb = f.get("size", 0) / 1024
        size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
        print(f"{f['filename']:<50} {f.get('rows', 0):>8} {size_str:>10} {f.get('created', '')}")


def cmd_download(args):
    """Download a result file."""
    s, base_url = _get_session(args)

    filename = None

    if args.job_id:
        # Get output files for this job
        resp = s.get(f"{base_url}/api/progress", params={"job_id": args.job_id}, allow_redirects=False)
        _check_response(resp, "Get job info")
        pdata = resp.json()
        output_files = pdata.get("output_files", [])
        if output_files:
            filename = output_files[0]
        else:
            _die(f"No output files for job {args.job_id}")
    elif args.file:
        filename = args.file
    else:
        # Get the latest result
        resp = s.get(f"{base_url}/api/list-results", allow_redirects=False)
        _check_response(resp, "List results")
        files = resp.json().get("files", [])
        if not files:
            _die("No result files available")
        filename = files[0]["filename"]

    out_path = args.output if args.output else filename

    dl_resp = s.get(f"{base_url}/api/download", params={"file": filename}, allow_redirects=False)
    _check_response(dl_resp, "Download")

    with open(out_path, "wb") as f:
        f.write(dl_resp.content)

    result = {
        "status": "ok",
        "filename": filename,
        "saved_to": out_path,
        "size": len(dl_resp.content),
    }
    _output(result, args.json)


def cmd_suggest(args):
    """Get AI-powered keyword/location suggestions."""
    s, base_url = _get_session(args)

    if not args.icp:
        _die("--icp is required")

    resp = s.post(
        f"{base_url}/api/ai-suggestions",
        json={"icp": args.icp},
        allow_redirects=False,
        timeout=120,
    )
    _check_response(resp, "AI suggestions")

    data = resp.json()
    if not data.get("success"):
        _die(data.get("error", "Unknown error"))

    if args.json:
        print(json.dumps(data, indent=2))
        return

    keywords = data.get("keywords", [])
    locations = data.get("locations", [])

    print(f"Keywords ({len(keywords)}):")
    print(f"  {','.join(keywords)}")
    print()
    print(f"Locations ({len(locations)}):")
    print(f"  {','.join(locations)}")

    # Print in a format ready to copy-paste into scrape command
    print()
    print("Ready-to-use scrape command:")
    kw_str = ",".join(keywords)
    loc_str = ",".join(locations)
    print(f'  yp-cli.py scrape --keywords "{kw_str}" --locations "{loc_str}" --wait')


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="yp-cli.py",
        description="CLI for the Yellow Pages Scraper API",
    )
    parser.add_argument("--url", help="Base URL of the scraper API (default: https://scrape-yp.mikehernandez.co)")
    parser.add_argument("--json", action="store_true", help="Output in JSON format (machine-readable)")

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # login
    p_login = sub.add_parser("login", help="Authenticate with the scraper API")
    p_login.add_argument("--user", required=True, help="Username")
    p_login.add_argument("--password", required=True, help="Password")

    # scrape
    p_scrape = sub.add_parser("scrape", help="Start a scraping job")
    p_scrape.add_argument("--keywords", required=True, help="Comma-separated search keywords")
    p_scrape.add_argument("--locations", required=True, help="Comma-separated locations (e.g. 'Miami FL,Houston TX')")
    p_scrape.add_argument("--pages", type=int, default=10, help="Max pages per search (default: 10)")
    p_scrape.add_argument("--concurrent", type=int, default=1, help="Concurrent browser instances (default: 1)")
    p_scrape.add_argument("--proxies", action="store_true", default=False, help="Use proxy rotation")
    p_scrape.add_argument("--wait", action="store_true", help="Wait for completion and auto-download results")
    p_scrape.add_argument("--output", "-o", help="Output file path (used with --wait)")

    # status
    p_status = sub.add_parser("status", help="Check job progress")
    p_status.add_argument("--job-id", help="Specific job ID (default: latest job)")

    # results
    sub.add_parser("results", help="List available result files")

    # download
    p_dl = sub.add_parser("download", help="Download a result file")
    p_dl.add_argument("--job-id", help="Download results for this job ID")
    p_dl.add_argument("--file", help="Specific filename to download")
    p_dl.add_argument("--output", "-o", help="Output file path (default: original filename)")

    # suggest
    p_suggest = sub.add_parser("suggest", help="Get AI keyword/location suggestions")
    p_suggest.add_argument("--icp", required=True, help="Ideal Customer Profile description")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "login": cmd_login,
        "scrape": cmd_scrape,
        "status": cmd_status,
        "results": cmd_results,
        "download": cmd_download,
        "suggest": cmd_suggest,
    }

    try:
        commands[args.command](args)
    except requests.ConnectionError:
        base_url = _get_base_url(args)
        _die(f"Cannot connect to {base_url}. Is the scraper API running?")
    except requests.Timeout:
        _die("Request timed out")
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
