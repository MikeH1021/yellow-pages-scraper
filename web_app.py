"""
Web UI for Yellow Pages Scraper
Stateless Flask frontend - all job state stored in Redis.
Scraping runs in separate worker pods.
"""

import logging
from flask import Flask, render_template, request, jsonify, Response, send_file, redirect, url_for, flash
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse
import json
import os
import re
from datetime import datetime
import time

import job_store

log = logging.getLogger(__name__)

RESULTS_DIR = os.environ.get('RESULTS_DIR', '/data/results')
PROXY_FILE = os.environ.get('PROXY_FILE', '/data/proxies/proxies.txt')
XAI_API_KEY = os.environ.get('XAI_API_KEY', '')
XAI_MODEL = os.environ.get('XAI_MODEL', 'grok-4.3')
HTM_API_KEY = os.environ.get('HTM_API_KEY', '')
HTM_BASE_URL = os.environ.get('HTM_BASE_URL', 'https://high-ticket-portal-production.up.railway.app')
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'yp-scraper-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'


class User(UserMixin):
    def __init__(self, username, password_hash, is_admin):
        self.id = username
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin

    @staticmethod
    def get_by_id(username):
        data = job_store.get_user(username)
        if data:
            return User(data['username'], data['password_hash'], data['is_admin'])
        return None

    @staticmethod
    def get_by_username(username):
        return User.get_by_id(username)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(username):
    return User.get_by_id(username)


def init_default_admin():
    users = job_store.list_users()
    if not users:
        admin_user = os.environ.get('ADMIN_USERNAME', 'mike')
        admin_pass = os.environ.get('ADMIN_PASSWORD', 'changeme123')
        password_hash = generate_password_hash(admin_pass)
        job_store.create_user(admin_user, password_hash, is_admin=True)
        print(f"Created default admin user: {admin_user}")


def init_app():
    for attempt in range(30):
        if job_store.ping():
            init_default_admin()
            return
        print(f'Waiting for Redis... (attempt {attempt + 1})')
        time.sleep(2)
    print('WARNING: Could not connect to Redis on startup')


init_app()


def _is_safe_redirect(target):
    """Validate redirect target is a safe relative URL."""
    if not target:
        return False
    parsed = urlparse(target)
    return not parsed.netloc and not parsed.scheme


def _validate_filename(filename):
    """Validate a result filename is safe."""
    if not filename:
        return None
    filename = os.path.basename(filename)
    if not re.match(r'^scrape_results_[a-zA-Z0-9_]+\.csv$', filename):
        return None
    return filename


# --- Health Check ---

@app.route('/healthz')
def healthz():
    if job_store.ping():
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "redis_down"}), 503


# --- Pages ---

@app.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('scraper.html')


@app.route('/docs')
@login_required
def docs():
    return render_template('docs.html')


@app.route('/changelog')
def changelog():
    return render_template('changelog.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if len(username) > 100 or len(password) > 200:
            flash('Invalid credentials', 'error')
            return render_template('login.html')

        user = User.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page and _is_safe_redirect(next_page):
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))

    users = job_store.list_users()
    return render_template('admin.html', users=users)


@app.route('/admin/add-user', methods=['POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    is_admin = request.form.get('is_admin') == 'on'

    if not username or not password:
        flash('Username and password are required', 'error')
        return redirect(url_for('admin'))

    if len(username) > 50 or not re.match(r'^[a-zA-Z0-9_.-]+$', username):
        flash('Username must be alphanumeric (max 50 chars)', 'error')
        return redirect(url_for('admin'))

    if len(password) < 6:
        flash('Password must be at least 6 characters', 'error')
        return redirect(url_for('admin'))

    password_hash = generate_password_hash(password)
    if job_store.create_user(username, password_hash, is_admin):
        flash(f'User "{username}" created successfully', 'success')
    else:
        flash('Username already exists', 'error')

    return redirect(url_for('admin'))


@app.route('/admin/delete-user/<username>', methods=['POST'])
@login_required
def delete_user(username):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403

    if username == current_user.username:
        flash('Cannot delete your own account', 'error')
        return redirect(url_for('admin'))

    # Prevent deleting last admin
    if job_store.count_admins() <= 1:
        user_data = job_store.get_user(username)
        if user_data and user_data.get('is_admin'):
            flash('Cannot delete the last admin user', 'error')
            return redirect(url_for('admin'))

    job_store.delete_user(username)
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin'))


@app.route('/settings')
@login_required
def settings():
    # Grok key (admin-only to change, all can see status)
    effective_xai = XAI_API_KEY or job_store.get_setting('xai_api_key', '')
    masked_key = ''
    key_source = ''
    if effective_xai:
        masked_key = effective_xai[:8] + '...' + effective_xai[-4:] if len(effective_xai) > 12 else '***'
        key_source = 'environment variable' if XAI_API_KEY else 'saved setting'

    # HTM key (per-user)
    user_htm_key = job_store.get_setting(f'htm_api_key:{current_user.username}', '')
    htm_masked = ''
    htm_source = ''
    if user_htm_key:
        htm_masked = user_htm_key[:8] + '...' + user_htm_key[-4:] if len(user_htm_key) > 12 else '***'
        htm_source = 'your personal key'
    elif HTM_API_KEY:
        htm_masked = HTM_API_KEY[:8] + '...' + HTM_API_KEY[-4:] if len(HTM_API_KEY) > 12 else '***'
        htm_source = 'global default'

    return render_template('settings.html',
        api_key_masked=masked_key, has_api_key=bool(effective_xai), key_source=key_source, model_name=XAI_MODEL,
        htm_key_masked=htm_masked, has_htm_key=bool(user_htm_key or HTM_API_KEY), htm_key_source=htm_source,
    )


@app.route('/settings/save', methods=['POST'])
@login_required
def save_settings():
    saved_something = False

    # Grok key — admin only
    xai_key = request.form.get('xai_api_key', '').strip()
    if xai_key and current_user.is_admin:
        job_store.set_setting('xai_api_key', xai_key)
        flash('Grok API key saved successfully', 'success')
        saved_something = True

    # HTM key — per user
    htm_key = request.form.get('htm_api_key', '').strip()
    if htm_key:
        job_store.set_setting(f'htm_api_key:{current_user.username}', htm_key)
        flash('HTM Portal API key saved successfully', 'success')
        saved_something = True

    if not saved_something:
        flash('No changes made', 'info')

    return redirect(url_for('settings'))


# --- API Endpoints ---

@app.route('/api/ai-suggestions', methods=['POST'])
@login_required
def ai_suggestions():
    """Get AI-powered keyword and location suggestions from Grok (xAI)"""
    try:
        import requests as http_requests

        data = request.json
        if not data:
            return jsonify({"error": "Invalid request"}), 400

        icp = data.get('icp', '').strip()

        if not icp:
            return jsonify({"error": "Please provide an Ideal Customer Profile"}), 400
        if len(icp) > 5000:
            return jsonify({"error": "ICP text is too long (max 5000 characters)"}), 400

        api_key = XAI_API_KEY or job_store.get_setting('xai_api_key')
        if not api_key:
            return jsonify({"error": "Grok API key not configured. Please add it in Settings or set XAI_API_KEY env var."}), 400

        prompt = f"""Based on the following Ideal Customer Profile (ICP), suggest business categories/keywords and US locations to search on Yellow Pages for lead generation.

ICP: {icp}

Provide your response in this exact JSON format:
{{
    "keywords": ["keyword1", "keyword2", ...],
    "locations": ["City ST", "City ST", ...]
}}

Rules:
- Keywords should be Yellow Pages business categories (e.g., "plumbers", "roofing contractors", "HVAC services")
- Provide up to 50 relevant keywords
- Locations should be in "City ST" format (e.g., "Miami FL", "Chicago IL")
- Provide up to 50 US locations that match the ICP's target market
- Focus on locations where the ICP's target customers are likely to be
- Only return the JSON object, no other text"""

        response = http_requests.post(
            'https://api.x.ai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': XAI_MODEL,
                'messages': [
                    {'role': 'system', 'content': 'You are a helpful assistant that provides business lead generation suggestions. Always respond with valid JSON only.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 2000
            },
            timeout=120
        )

        if response.status_code != 200:
            try:
                error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            except Exception:
                error_msg = f"HTTP {response.status_code}"
            return jsonify({"error": f"Grok API error: {error_msg}"}), 500

        result = response.json()

        try:
            content = result['choices'][0]['message']['content'].strip()
        except (KeyError, IndexError, TypeError):
            return jsonify({"error": "Unexpected response format from Grok API"}), 500

        if content.startswith('```'):
            parts = content.split('```')
            content = parts[1] if len(parts) > 1 else content
            if content.startswith('json'):
                content = content[4:]
        content = content.strip()

        suggestions = json.loads(content)
        keywords = suggestions.get('keywords', [])
        locations = suggestions.get('locations', [])

        if not isinstance(keywords, list):
            keywords = []
        if not isinstance(locations, list):
            locations = []

        return jsonify({
            "success": True,
            "keywords": keywords,
            "locations": locations,
            "keyword_count": len(keywords),
            "location_count": len(locations)
        })

    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse AI response. Please try again."}), 500
    except Exception as e:
        log.exception("AI suggestions error")
        return jsonify({"error": "Failed to get suggestions. Please try again."}), 500


# --- HTM Portal Integration ---

def _get_htm_key():
    """Get HTM API key — per-user first, then global env var."""
    if current_user.is_authenticated:
        user_key = job_store.get_setting(f'htm_api_key:{current_user.username}')
        if user_key:
            return user_key
    return HTM_API_KEY


def _htm_request(path, params=None):
    """Make an authenticated request to the HTM Portal API."""
    import requests as http_requests
    api_key = _get_htm_key()
    if not api_key:
        return None, "HTM Portal API key not set. Add it in Settings."
    try:
        resp = http_requests.get(
            f"{HTM_BASE_URL}{path}",
            headers={'Authorization': f'Bearer {api_key}'},
            params=params,
            timeout=30,
        )
        if resp.status_code == 401:
            return None, "HTM Portal API key is invalid. Check your key in Settings."
        if not resp.ok:
            return None, f"HTM Portal error: HTTP {resp.status_code}"
        return resp.json(), None
    except Exception as e:
        log.exception("HTM Portal request failed")
        return None, f"Failed to connect to HTM Portal"


@app.route('/api/htm/clients')
@login_required
def htm_clients():
    """Search clients from HTM Portal."""
    q = request.args.get('q', '').strip()
    params = {'fields': 'name,strategist,csm,stage'}
    if q and len(q) >= 2:
        params['q'] = q
    data, err = _htm_request('/api/v1/clients', params)
    if err:
        return jsonify({"error": err}), 400
    clients = [{'name': c.get('name', ''), 'strategist': c.get('strategist', ''), 'csm': c.get('csm', ''), 'stage': c.get('stage', '')} for c in data.get('clients', [])]
    return jsonify({"success": True, "clients": clients, "total": len(clients)})


@app.route('/api/htm/client-data')
@login_required
def htm_client_data():
    """Fetch client context (ICP) and documents from HTM Portal."""
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify({"error": "Client name required"}), 400

    from urllib.parse import quote
    encoded_name = quote(name, safe='')

    # Fetch context (ICP, transcript notes, requirements)
    ctx_data, ctx_err = _htm_request(f'/api/v1/clients/{encoded_name}/context')
    context = {}
    if ctx_data and isinstance(ctx_data, dict):
        context = ctx_data.get('context') or {}

    # Fetch documents
    doc_data, doc_err = _htm_request(f'/api/v1/clients/{encoded_name}/documents', {'includeText': 'true'})
    documents = []
    if doc_data and isinstance(doc_data, dict):
        documents = doc_data.get('documents') or []

    if ctx_err and doc_err:
        return jsonify({"error": ctx_err}), 400

    return jsonify({
        "success": True,
        "clientName": name,
        "context": {
            "icpSummary": context.get('icpSummary') or '',
            "specialRequirements": context.get('specialRequirements') or '',
            "transcriptNotes": context.get('transcriptNotes') or '',
        },
        "documents": [
            {
                "id": d.get('id', ''),
                "name": d.get('originalName', d.get('name', '')),
                "text": (d.get('extractedText') or '')[:5000],
            }
            for d in documents if isinstance(d, dict)
        ],
    })


@app.route('/api/htm/generate-lists', methods=['POST'])
@login_required
def htm_generate_lists():
    """Use Grok to analyze client data and suggest 5 scrape lists."""
    try:
        import requests as http_requests

        data = request.json
        if not data:
            return jsonify({"error": "Invalid request"}), 400

        client_name = data.get('clientName', '')
        icp_summary = data.get('icpSummary', '')
        transcript_notes = data.get('transcriptNotes', '')
        special_requirements = data.get('specialRequirements', '')
        document_texts = data.get('documentTexts', [])

        # Build context block
        context_parts = []
        if icp_summary:
            context_parts.append(f"ICP SUMMARY:\n{icp_summary}")
        if transcript_notes:
            context_parts.append(f"STRATEGY CALL NOTES:\n{transcript_notes}")
        if special_requirements:
            context_parts.append(f"SPECIAL REQUIREMENTS:\n{special_requirements}")
        for i, doc in enumerate(document_texts[:3]):
            if doc.get('text'):
                doc_name = doc.get('name', f'Doc {i+1}')
                context_parts.append(f"DOCUMENT '{doc_name}':\n{doc['text'][:3000]}")

        if not context_parts:
            return jsonify({"error": "No client data available. Upload documents or set ICP in the portal first."}), 400

        full_context = "\n\n---\n\n".join(context_parts)

        api_key = XAI_API_KEY or job_store.get_setting('xai_api_key')
        if not api_key:
            return jsonify({"error": "Grok API key not configured"}), 400

        prompt = f"""You are a B2B lead generation expert. Analyze the following client strategy data and propose exactly 5 distinct Yellow Pages scrape lists.

CLIENT: {client_name}

{full_context}

---

Based on this information, create 5 DIFFERENT scrape lists that each target a distinct segment of the client's ideal customer profile. Each list should approach the ICP from a different angle — different industries, different roles, different geographic focuses, or different service categories.

Respond in this exact JSON format:
{{
  "lists": [
    {{
      "name": "Short descriptive name for this list",
      "description": "1-2 sentence explanation of what this list targets and why",
      "keywords": ["keyword1", "keyword2", "keyword3", ...],
      "locations": ["City ST", "City ST", ...],
      "estimated_results": "rough estimate like '5,000-10,000'"
    }},
    ...
  ]
}}

Rules:
- Each list MUST have a unique targeting angle (don't just repeat the same keywords with different cities)
- Keywords should be Yellow Pages business categories (e.g., "plumbers", "roofing contractors")
- Locations in "City ST" format (e.g., "Miami FL", "Chicago IL")
- Include 5-20 keywords per list
- Include 5-30 locations per list
- Consider the client's geographic preferences from the strategy data
- Think about adjacent industries and related service providers
- Only return valid JSON, no other text"""

        response = http_requests.post(
            'https://api.x.ai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': XAI_MODEL,
                'messages': [
                    {'role': 'system', 'content': 'You are a B2B lead generation strategist. Always respond with valid JSON only.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.8,
                'max_tokens': 4000
            },
            timeout=120
        )

        if response.status_code != 200:
            try:
                error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            except Exception:
                error_msg = f"HTTP {response.status_code}"
            return jsonify({"error": f"Grok API error: {error_msg}"}), 500

        result = response.json()
        try:
            content = result['choices'][0]['message']['content'].strip()
        except (KeyError, IndexError, TypeError):
            return jsonify({"error": "Unexpected response from Grok"}), 500

        if content.startswith('```'):
            parts = content.split('```')
            content = parts[1] if len(parts) > 1 else content
            if content.startswith('json'):
                content = content[4:]
        content = content.strip()

        suggestions = json.loads(content)
        lists = suggestions.get('lists', [])

        if not isinstance(lists, list) or len(lists) == 0:
            return jsonify({"error": "Grok did not return valid list suggestions"}), 500

        return jsonify({"success": True, "lists": lists[:5], "clientName": client_name})

    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse AI response. Please try again."}), 500
    except Exception as e:
        log.exception("HTM generate lists error")
        return jsonify({"error": "Failed to generate lists. Please try again."}), 500


@app.route('/api/upload-proxies', methods=['POST'])
@login_required
def upload_proxies():
    """Handle proxy file upload - saves to shared volume for workers."""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        os.makedirs(os.path.dirname(PROXY_FILE), exist_ok=True)
        file.save(PROXY_FILE)

        proxy_count = 0
        with open(PROXY_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    proxy_count += 1

        return jsonify({
            "success": True,
            "proxy_count": proxy_count,
            "message": f"Loaded {proxy_count} proxies"
        })

    except Exception as e:
        log.exception("Proxy upload error")
        return jsonify({"error": "Failed to upload proxy file"}), 500


@app.route('/api/proxy-status')
@login_required
def proxy_status():
    proxies = []
    try:
        if os.path.exists(PROXY_FILE):
            with open(PROXY_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(':')
                        if len(parts) >= 2:
                            proxies.append({
                                "host": parts[0],
                                "port": parts[1],
                                "success_count": 0,
                                "fail_count": 0,
                                "success_rate": 1.0,
                                "is_blocked": False,
                                "last_used": "N/A"
                            })
    except Exception:
        pass
    return jsonify({"proxies": proxies})


@app.route('/api/start-scrape', methods=['POST'])
@login_required
def start_scrape():
    """Submit a new scraping job to Redis for workers to pick up."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid request"}), 400

        keywords = [k.strip()[:100] for k in data.get('keywords', '').split(',') if k.strip()]
        locations = [l.strip()[:100] for l in data.get('locations', '').split(',') if l.strip()]

        if not keywords or not locations:
            return jsonify({"error": "Please provide keywords and locations"}), 400
        if len(keywords) > 200:
            return jsonify({"error": "Maximum 200 keywords allowed"}), 400
        if len(locations) > 200:
            return jsonify({"error": "Maximum 200 locations allowed"}), 400

        try:
            max_pages = max(1, min(int(data.get('max_pages', 10)), 100))
            max_businesses = max(0, min(int(data.get('max_businesses', 0)), 1000000))
            concurrent = max(1, min(int(data.get('concurrent', 1)), 500))
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid numeric parameters"}), 400

        use_proxies = bool(data.get('use_proxies', True))
        chunk_output = bool(data.get('chunk_output', False))

        total_searches = len(keywords) * len(locations)
        if total_searches > 10000:
            return jsonify({"error": f"Too many searches ({total_searches:,}). Maximum is 10,000."}), 400

        searches = []
        for location in locations:
            for keyword in keywords:
                searches.append({"term": keyword, "location": location})

        if not job_store.ping():
            return jsonify({"error": "Service temporarily unavailable. Please try again."}), 503

        job_id = job_store.create_job(
            searches=searches,
            max_pages=max_pages,
            use_proxies=use_proxies,
            concurrent=concurrent,
            chunk_output=chunk_output,
            max_businesses=max_businesses,
            username=current_user.username,
        )

        return jsonify({
            "success": True,
            "job_id": job_id,
            "total_searches": len(searches),
            "message": f"Job {job_id} queued with {len(searches)} searches"
        })

    except Exception as e:
        log.exception("Start scrape error")
        return jsonify({"error": "Failed to start scrape. Please try again."}), 500


@app.route('/api/stop-scrape', methods=['POST'])
@login_required
def stop_scrape():
    data = request.json or {}
    job_id = data.get('job_id')

    if not job_id:
        jobs = job_store.get_user_jobs(current_user.username)
        for j in jobs:
            if j.get('status') in ('running', 'pending'):
                job_id = j.get('job_id')
                break

    if job_id:
        job_store.stop_job(job_id)
        return jsonify({"success": True, "message": f"Job {job_id} stopping"})

    return jsonify({"success": True, "message": "No running job found"})


@app.route('/api/progress')
@login_required
def get_progress():
    job_id = request.args.get('job_id')

    if not job_id:
        jobs = job_store.get_user_jobs(current_user.username, limit=1)
        if jobs:
            job_id = jobs[0].get('job_id')

    if not job_id:
        return jsonify({"running": False, "progress": {}, "output_files": []})

    job = job_store.get_job(job_id)
    if not job:
        return jsonify({"running": False, "progress": {}, "output_files": []})

    status = job.get('status', 'unknown')
    running = status in ('pending', 'running')
    return jsonify({
        "running": running,
        "job_id": job_id,
        "status": status,
        "progress": {
            "total_searches": job.get('total_searches', 0),
            "completed": job.get('completed', 0),
            "businesses_found": job.get('businesses_found', 0),
            "errors": job.get('errors', 0),
            "max_businesses": job.get('max_businesses', 0),
            "limit_reached": job.get('limit_reached', False),
        },
        "output_files": job.get('output_files', []),
        "last_output_file": job['output_files'][0] if job.get('output_files') else None,
    })


@app.route('/api/download')
@login_required
def download_results():
    try:
        filename = _validate_filename(request.args.get('file'))
        if not filename:
            return jsonify({"error": "Invalid or missing filename"}), 400

        filepath = os.path.join(RESULTS_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404

        return send_file(filepath, as_attachment=True, download_name=filename, mimetype='text/csv')

    except Exception as e:
        log.exception("Download error")
        return jsonify({"error": "Download failed"}), 500


@app.route('/api/download-all')
@login_required
def download_all_results():
    try:
        import zipfile
        from io import BytesIO

        job_id = request.args.get('job_id')
        if not job_id:
            jobs = job_store.get_user_jobs(current_user.username, limit=1)
            if jobs:
                job_id = jobs[0].get('job_id')

        if not job_id:
            return jsonify({"error": "No results available"}), 404

        job = job_store.get_job(job_id)
        if not job or not job.get('output_files'):
            return jsonify({"error": "No results available"}), 404

        output_files = [f for f in job['output_files'] if _validate_filename(f)]

        if len(output_files) == 1:
            filepath = os.path.join(RESULTS_DIR, output_files[0])
            if os.path.exists(filepath):
                return send_file(filepath, as_attachment=True, download_name=output_files[0], mimetype='text/csv')
            return jsonify({"error": "File not found"}), 404

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for fname in output_files:
                fpath = os.path.join(RESULTS_DIR, fname)
                if os.path.exists(fpath):
                    zf.write(fpath, fname)

        zip_buffer.seek(0)
        return send_file(zip_buffer, as_attachment=True, download_name=f"scrape_results_{timestamp}.zip", mimetype='application/zip')

    except Exception as e:
        log.exception("Download all error")
        return jsonify({"error": "Download failed"}), 500


@app.route('/api/list-results')
@login_required
def list_results():
    try:
        csv_files = []
        os.makedirs(RESULTS_DIR, exist_ok=True)

        for file in os.listdir(RESULTS_DIR):
            if not _validate_filename(file):
                continue
            filepath = os.path.join(RESULTS_DIR, file)
            stat = os.stat(filepath)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    row_count = sum(1 for _ in f) - 1
            except Exception:
                row_count = 0

            csv_files.append({
                "filename": file,
                "size": stat.st_size,
                "rows": max(0, row_count),
                "created": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })

        csv_files.sort(key=lambda x: x['created'], reverse=True)
        return jsonify({"files": csv_files})

    except Exception as e:
        log.exception("List results error")
        return jsonify({"error": "Failed to list results"}), 500


@app.route('/api/delete-result', methods=['POST'])
@login_required
def delete_result():
    try:
        data = request.json
        filename = _validate_filename(data.get('filename', '') if data else '')
        if not filename:
            return jsonify({"error": "Invalid filename"}), 400

        filepath = os.path.join(RESULTS_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404

        os.remove(filepath)
        return jsonify({"success": True, "message": f"Deleted {filename}"})

    except Exception as e:
        log.exception("Delete result error")
        return jsonify({"error": "Failed to delete file"}), 500


@app.route('/api/clear-results', methods=['POST'])
@login_required
def clear_results():
    try:
        deleted = 0
        os.makedirs(RESULTS_DIR, exist_ok=True)
        for file in os.listdir(RESULTS_DIR):
            if _validate_filename(file):
                os.remove(os.path.join(RESULTS_DIR, file))
                deleted += 1

        return jsonify({"success": True, "deleted": deleted})

    except Exception as e:
        log.exception("Clear results error")
        return jsonify({"error": "Failed to clear results"}), 500


@app.route('/api/logs')
@login_required
def stream_logs():
    """SSE endpoint for real-time logs - reads from Redis with timeout protection."""
    job_id = request.args.get('job_id')

    if not job_id:
        jobs = job_store.get_user_jobs(current_user.username, limit=1)
        if jobs:
            job_id = jobs[0].get('job_id')

    MAX_STREAM_SECONDS = 3600  # 1 hour max SSE connection

    def generate():
        if not job_id:
            yield f"data: {json.dumps({'heartbeat': True})}\n\n"
            return

        # Replay history first
        try:
            history = job_store.get_log_history(job_id)
            for entry in history:
                yield f"data: {json.dumps(entry)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'level': 'error', 'message': 'Failed to load log history', 'timestamp': time.strftime('%H:%M:%S')})}\n\n"

        # Subscribe for live updates
        pubsub = None
        try:
            pubsub = job_store.subscribe_logs(job_id)
            start_time = time.time()
            last_heartbeat = time.time()
            consecutive_errors = 0

            while True:
                # Timeout protection
                if time.time() - start_time > MAX_STREAM_SECONDS:
                    yield f"data: {json.dumps({'level': 'info', 'message': 'Log stream timed out. Refresh to reconnect.', 'timestamp': time.strftime('%H:%M:%S')})}\n\n"
                    break

                try:
                    msg = pubsub.get_message(timeout=1.0)
                    consecutive_errors = 0

                    if msg and msg['type'] == 'message':
                        yield f"data: {msg['data']}\n\n"
                        last_heartbeat = time.time()
                    elif time.time() - last_heartbeat > 3:
                        yield f"data: {json.dumps({'heartbeat': True})}\n\n"
                        last_heartbeat = time.time()
                except Exception:
                    consecutive_errors += 1
                    if consecutive_errors > 5:
                        yield f"data: {json.dumps({'level': 'error', 'message': 'Lost connection to log stream', 'timestamp': time.strftime('%H:%M:%S')})}\n\n"
                        break
                    time.sleep(1)
                    continue

                # Check if job is done (every ~3 seconds via heartbeat cycle)
                if time.time() - last_heartbeat >= 0:
                    try:
                        job = job_store.get_job(job_id)
                        if job and job.get('status') not in ('pending', 'running'):
                            time.sleep(1)
                            # Flush any remaining messages
                            for _ in range(10):
                                msg = pubsub.get_message(timeout=0.1)
                                if msg and msg['type'] == 'message':
                                    yield f"data: {msg['data']}\n\n"
                            yield f"data: {json.dumps({'job_complete': True, 'status': job.get('status')})}\n\n"
                            break
                    except Exception:
                        pass
        finally:
            if pubsub:
                try:
                    pubsub.close()
                except Exception:
                    pass

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    import socket

    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "your-vm-ip"

    print("=" * 60)
    print("Yellow Pages Scraper Web UI")
    print("=" * 60)
    print(f"\nServer running on: http://0.0.0.0:5001")
    print(f"Access via: http://{local_ip}:5001")
    print("=" * 60)

    app.run(host='0.0.0.0', debug=True, port=5001, threaded=True)
