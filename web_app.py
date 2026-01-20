"""
Web UI for Yellow Pages Scraper
Simple interface for configuring and running scrapes with real-time monitoring
"""

from flask import Flask, render_template, request, jsonify, Response, send_file
from flask_cors import CORS
import asyncio
import json
import os
import threading
from datetime import datetime
from queue import Queue
import time

from yellowpages_scraper import YellowPagesScraper
from proxy_manager import ProxyManager

app = Flask(__name__)
CORS(app)

# Global state
scraper_state = {
    "running": False,
    "progress": {},
    "log_queue": Queue(),
    "proxy_manager": None,
    "current_scraper": None,
    "last_output_file": None
}

class WebLogger:
    """Logger that pushes to web UI"""
    def __init__(self, log_queue):
        self.log_queue = log_queue

    def info(self, message):
        self.log_queue.put({
            "level": "info",
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

    def error(self, message):
        self.log_queue.put({
            "level": "error",
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

    def success(self, message):
        self.log_queue.put({
            "level": "success",
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

@app.route('/')
def index():
    """Main scraper interface"""
    return render_template('scraper.html')

@app.route('/api/upload-proxies', methods=['POST'])
def upload_proxies():
    """Handle proxy file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save to proxies.txt
        file.save('proxies.txt')

        # Reload proxy manager
        scraper_state["proxy_manager"] = ProxyManager.from_file('proxies.txt', validate=False)

        proxy_count = len(scraper_state["proxy_manager"].proxies)

        return jsonify({
            "success": True,
            "proxy_count": proxy_count,
            "message": f"Loaded {proxy_count} proxies"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/proxy-status')
def proxy_status():
    """Get current proxy health status"""
    if not scraper_state["proxy_manager"]:
        return jsonify({"proxies": []})

    proxies = []
    for proxy in scraper_state["proxy_manager"].proxies:
        proxies.append({
            "host": proxy.host,
            "port": proxy.port,
            "success_count": proxy.success_count,
            "fail_count": proxy.fail_count,
            "success_rate": proxy.get_success_rate(),
            "is_blocked": proxy.is_blocked,
            "last_used": proxy.last_used.strftime("%H:%M:%S") if proxy.last_used else "Never"
        })

    return jsonify({"proxies": proxies})

@app.route('/api/start-scrape', methods=['POST'])
def start_scrape():
    """Start a new scraping job"""
    try:
        data = request.json

        # Parse comma-separated inputs
        keywords = [k.strip() for k in data.get('keywords', '').split(',') if k.strip()]
        locations = [l.strip() for l in data.get('locations', '').split(',') if l.strip()]

        if not keywords or not locations:
            return jsonify({"error": "Please provide keywords and locations"}), 400

        max_pages = int(data.get('max_pages', 10))
        use_proxies = data.get('use_proxies', True)
        concurrent = int(data.get('concurrent', 1))

        # Build search list
        searches = []
        for location in locations:
            for keyword in keywords:
                searches.append({
                    "term": keyword,
                    "location": location
                })

        # Update state
        scraper_state["running"] = True
        scraper_state["progress"] = {
            "total_searches": len(searches),
            "completed": 0,
            "businesses_found": 0
        }

        # Clear log queue
        while not scraper_state["log_queue"].empty():
            scraper_state["log_queue"].get()

        # Start scraper in background thread
        thread = threading.Thread(
            target=run_scraper_async,
            args=(searches, max_pages, use_proxies, concurrent)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            "success": True,
            "total_searches": len(searches),
            "message": f"Started scraping {len(searches)} searches"
        })

    except Exception as e:
        scraper_state["running"] = False
        return jsonify({"error": str(e)}), 500

@app.route('/api/stop-scrape', methods=['POST'])
def stop_scrape():
    """Stop current scraping job"""
    scraper_state["running"] = False
    return jsonify({"success": True, "message": "Scraper stopped"})

@app.route('/api/progress')
def get_progress():
    """Get current scraping progress"""
    return jsonify({
        "running": scraper_state["running"],
        "progress": scraper_state["progress"],
        "last_output_file": scraper_state.get("last_output_file")
    })

@app.route('/api/download')
def download_results():
    """Download CSV file - either specific file or last generated"""
    try:
        # Check if specific file requested
        filename = request.args.get('file')

        if filename:
            # Download specific file
            if not filename.startswith('scrape_results_') or not filename.endswith('.csv'):
                return jsonify({"error": "Invalid filename"}), 400

            if not os.path.exists(filename):
                return jsonify({"error": "File not found"}), 404

            output_file = filename
        else:
            # Download last generated file
            output_file = scraper_state.get("last_output_file")

            if not output_file:
                return jsonify({"error": "No results available to download"}), 404

            if not os.path.exists(output_file):
                return jsonify({"error": "Result file not found"}), 404

        return send_file(
            output_file,
            as_attachment=True,
            download_name=os.path.basename(output_file),
            mimetype='text/csv'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/list-results')
def list_results():
    """List all available CSV result files"""
    try:
        csv_files = []
        for file in os.listdir('.'):
            if file.startswith('scrape_results_') and file.endswith('.csv'):
                stat = os.stat(file)
                csv_files.append({
                    "filename": file,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                })

        # Sort by creation time, newest first
        csv_files.sort(key=lambda x: x['created'], reverse=True)

        return jsonify({"files": csv_files})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/logs')
def stream_logs():
    """Server-Sent Events endpoint for real-time logs"""
    def generate():
        while True:
            if not scraper_state["log_queue"].empty():
                log = scraper_state["log_queue"].get()
                yield f"data: {json.dumps(log)}\n\n"
            else:
                # Send heartbeat
                yield f"data: {json.dumps({'heartbeat': True})}\n\n"
            time.sleep(0.1)

    return Response(generate(), mimetype='text/event-stream')

def run_scraper_async(searches, max_pages, use_proxies, concurrent=1):
    """Run scraper in async context"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_scraper(searches, max_pages, use_proxies, concurrent))

async def run_single_search(search, max_pages, proxy_manager, search_num, total_searches):
    """Run a single search (used for parallel processing)"""
    logger = WebLogger(scraper_state["log_queue"])

    try:
        # Create separate scraper instance for this search
        scraper = YellowPagesScraper(
            headless=True,
            delay=3.0,
            proxy_manager=proxy_manager
        )

        await scraper.start_browser()

        logger.info(f"[{search_num}/{total_searches}] {search['term']} in {search['location']}")

        businesses = await scraper.scrape_search(
            search_term=search['term'],
            location=search['location'],
            max_pages=max_pages
        )

        # Tag with search info
        for biz in businesses:
            biz['search_category'] = search['term']
            biz['search_location'] = search['location']

        logger.success(f"✓ [{search_num}/{total_searches}] Found {len(businesses)} businesses")

        await scraper.close_browser()

        return businesses

    except Exception as e:
        logger.error(f"❌ [{search_num}/{total_searches}] Error: {str(e)}")
        return []

async def run_scraper(searches, max_pages, use_proxies, concurrent=1):
    """Main scraping logic - supports both sequential and parallel"""
    logger = WebLogger(scraper_state["log_queue"])
    all_businesses = []

    try:
        logger.info(f"🚀 Starting scraper... (Concurrency: {concurrent})")

        # Setup proxy manager
        proxy_manager = None
        if use_proxies:
            if scraper_state["proxy_manager"] and scraper_state["proxy_manager"].proxies:
                proxy_manager = scraper_state["proxy_manager"]
                logger.success(f"✅ Using {len(proxy_manager.proxies)} proxies")
            else:
                logger.error("⚠️ No proxies loaded - running without proxies")

        if concurrent == 1:
            # Sequential mode (original behavior)
            scraper = YellowPagesScraper(
                headless=True,
                delay=3.0,
                proxy_manager=proxy_manager
            )

            scraper_state["current_scraper"] = scraper

            await scraper.start_browser()
            logger.success("✅ Browser started")

            # Run searches sequentially
            for i, search in enumerate(searches, 1):
                if not scraper_state["running"]:
                    logger.info("⚠️ Scraper stopped by user")
                    break

                logger.info(f"[{i}/{len(searches)}] {search['term']} in {search['location']}")

                businesses = await scraper.scrape_search(
                    search_term=search['term'],
                    location=search['location'],
                    max_pages=max_pages
                )

                # Tag with search info
                for biz in businesses:
                    biz['search_category'] = search['term']
                    biz['search_location'] = search['location']

                all_businesses.extend(businesses)

                # Update progress
                scraper_state["progress"]["completed"] = i
                scraper_state["progress"]["businesses_found"] = len(all_businesses)

                logger.success(f"✓ Found {len(businesses)} businesses (Total: {len(all_businesses)})")

            await scraper.close_browser()

        else:
            # Parallel mode
            logger.success(f"✅ Running {concurrent} searches in parallel")

            import asyncio

            # Process searches in batches
            for batch_num, i in enumerate(range(0, len(searches), concurrent), 1):
                if not scraper_state["running"]:
                    logger.info("⚠️ Scraper stopped by user")
                    break

                batch = searches[i:i + concurrent]
                batch_size = len(batch)

                logger.info(f"📦 Batch {batch_num}: Processing {batch_size} searches in parallel...")

                # Create tasks for parallel execution
                tasks = [
                    run_single_search(
                        search=search,
                        max_pages=max_pages,
                        proxy_manager=proxy_manager,
                        search_num=i + j + 1,
                        total_searches=len(searches)
                    )
                    for j, search in enumerate(batch)
                ]

                # Run all searches in this batch concurrently
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)

                # Collect results
                for result in batch_results:
                    if isinstance(result, list):
                        all_businesses.extend(result)

                # Update progress
                scraper_state["progress"]["completed"] = min(i + concurrent, len(searches))
                scraper_state["progress"]["businesses_found"] = len(all_businesses)

                logger.success(f"✓ Batch {batch_num} complete! Total businesses: {len(all_businesses)}")

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"scrape_results_{timestamp}.csv"

        from yellowpages_scraper import YellowPagesScraper
        temp_scraper = YellowPagesScraper()
        temp_scraper.save_to_csv(all_businesses, output_file)

        # Store filename for download
        scraper_state["last_output_file"] = output_file

        logger.success(f"✅ COMPLETE! Saved {len(all_businesses)} businesses to {output_file}")
        logger.success(f"📥 Click 'Download Results' button to save to your computer")

    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        if concurrent == 1 and scraper_state.get("current_scraper"):
            await scraper_state["current_scraper"].close_browser()
        scraper_state["running"] = False

if __name__ == '__main__':
    print("=" * 60)
    print("Yellow Pages Scraper Web UI")
    print("=" * 60)
    print("\nStarting server at: http://localhost:5001")
    print("\nOpen your browser and navigate to http://localhost:5001")
    print("=" * 60)

    app.run(debug=True, port=5001, threaded=True)
