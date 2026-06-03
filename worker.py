"""
Scrape worker process. Runs independently from the web server.
Polls Redis for scrape jobs, runs shared-browser scraper, publishes results.
"""

import asyncio
import os
import signal
import sys
import time
import math
import logging
from datetime import datetime

import pandas as pd

import job_store
import browser_scraper
from proxy_manager import ProxyManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [worker] %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
)
log = logging.getLogger(__name__)

MAX_CONCURRENT = int(os.environ.get('MAX_CONCURRENT', '50'))
RESULTS_DIR = os.environ.get('RESULTS_DIR', '/data/results')
PROXY_FILE = os.environ.get('PROXY_FILE', '')
POLL_INTERVAL = int(os.environ.get('POLL_INTERVAL', '2'))
JOB_TIMEOUT = int(os.environ.get('JOB_TIMEOUT', '3600'))  # 1 hour max per job

shutdown_requested = False


def handle_signal(signum, frame):
    global shutdown_requested
    log.info('Shutdown signal received, will exit after current job')
    shutdown_requested = True


signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)


class WorkerLogger:
    """Publishes logs to Redis for a specific job."""
    def __init__(self, job_id):
        self.job_id = job_id

    def info(self, msg):
        job_store.publish_log(self.job_id, 'info', msg)
        log.info(f'[{self.job_id}] {msg}')

    def error(self, msg):
        job_store.publish_log(self.job_id, 'error', msg)
        log.error(f'[{self.job_id}] {msg}')

    def success(self, msg):
        job_store.publish_log(self.job_id, 'success', msg)
        log.info(f'[{self.job_id}] {msg}')


def save_chunked_csv(businesses, base_filepath, chunk_size=50000):
    if not businesses:
        return []

    output_files = []
    total_rows = len(businesses)
    num_chunks = math.ceil(total_rows / chunk_size)

    if num_chunks == 1:
        df = pd.DataFrame(businesses)
        df.to_csv(base_filepath, index=False, encoding='utf-8')
        output_files.append(os.path.basename(base_filepath))
    else:
        for i in range(num_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, total_rows)
            chunk = businesses[start_idx:end_idx]
            name_parts = base_filepath.rsplit('.', 1)
            chunk_path = f"{name_parts[0]}_part{i+1}of{num_chunks}.csv"
            df = pd.DataFrame(chunk)
            df.to_csv(chunk_path, index=False, encoding='utf-8')
            output_files.append(os.path.basename(chunk_path))

    return output_files


async def process_job(job_id):
    """Process a single scrape job with full error handling."""
    job = job_store.get_job(job_id)
    if not job:
        log.warning(f'Job {job_id} not found, skipping')
        return

    logger = WorkerLogger(job_id)
    searches = job['searches']
    max_pages = job['max_pages']
    concurrent = min(job['concurrent'], MAX_CONCURRENT)
    use_proxies = job['use_proxies']
    chunk_output = job['chunk_output']
    max_businesses = job['max_businesses']

    job_store.update_job(job_id, status='running')
    logger.info(f"Starting job: {len(searches)} searches, concurrency={concurrent}")
    logger.info(f"Engine: shared-browser (1 Chromium + {concurrent} concurrent contexts)")

    if max_businesses > 0:
        logger.info(f"Business limit: {max_businesses:,}")

    # Setup proxy manager
    proxy_manager = None
    if use_proxies and PROXY_FILE and os.path.exists(PROXY_FILE):
        proxy_manager = ProxyManager.from_file(PROXY_FILE, validate=False)
        if proxy_manager.proxies:
            logger.success(f"Using {len(proxy_manager.proxies)} proxies")
        else:
            logger.error("No proxies loaded - running without proxies")
            proxy_manager = None

    stop_flag = False

    total_biz_count = 0

    def on_result(completed, total, businesses, error_count):
        nonlocal stop_flag, total_biz_count
        biz_count = len(businesses)
        total_biz_count += biz_count

        job_store.update_job(
            job_id,
            completed=completed,
            businesses_found=total_biz_count,
            errors=error_count,
        )

        if biz_count > 0:
            logger.success(f"[{completed}/{total}] Found {biz_count} businesses (Total: {total_biz_count:,})")
        elif error_count > 0 and completed % 10 == 0:
            logger.info(f"[{completed}/{total}] {error_count} errors so far")

        if max_businesses > 0 and total_biz_count >= max_businesses:
            stop_flag = True

    def on_error(search_num, total, error_msg):
        job_store.increment_job_errors(job_id)
        logger.error(f"[{search_num}/{total}] {error_msg}")

    def stop_check():
        if stop_flag:
            return True
        if shutdown_requested:
            return True
        return job_store.is_job_stopping(job_id)

    try:
        all_businesses = await asyncio.wait_for(
            browser_scraper.scrape_batch(
                searches=searches,
                max_pages=max_pages,
                proxy_manager=proxy_manager,
                max_concurrent=concurrent,
                delay=1.5,
                on_result=on_result,
                on_error=on_error,
                stop_check=stop_check,
            ),
            timeout=JOB_TIMEOUT,
        )

        # Apply business limit
        if max_businesses > 0 and len(all_businesses) > max_businesses:
            all_businesses = all_businesses[:max_businesses]
            job_store.update_job(job_id, limit_reached=True)
            logger.success(f"Applied business limit ({max_businesses:,})")

        # Save results
        os.makedirs(RESULTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"scrape_results_{job_id}_{timestamp}.csv"
        base_filepath = os.path.join(RESULTS_DIR, base_filename)

        if all_businesses:
            try:
                if chunk_output:
                    output_files = save_chunked_csv(all_businesses, base_filepath)
                else:
                    df = pd.DataFrame(all_businesses)
                    df.to_csv(base_filepath, index=False, encoding='utf-8')
                    output_files = [base_filename]

                job_store.update_job(
                    job_id,
                    status='complete',
                    output_files=output_files,
                    businesses_found=len(all_businesses),
                    completed=len(searches),
                )
                logger.success(f"COMPLETE! Saved {len(all_businesses):,} businesses to {len(output_files)} file(s)")
            except OSError as e:
                logger.error(f"Failed to save CSV: {e}")
                job_store.update_job(job_id, status='error')
                # Clean up partial file
                try:
                    if os.path.exists(base_filepath):
                        os.remove(base_filepath)
                except OSError:
                    pass
        else:
            job_store.update_job(job_id, status='complete', completed=len(searches))
            logger.info("Job complete - no businesses found")

    except asyncio.TimeoutError:
        logger.error(f"Job timed out after {JOB_TIMEOUT}s")
        job_store.update_job(job_id, status='error')
    except asyncio.CancelledError:
        logger.info("Job cancelled (worker shutting down)")
        job_store.update_job(job_id, status='error')
    except Exception as e:
        logger.error(f"Job failed: {e}")
        job_store.update_job(job_id, status='error')
        log.exception(f"Job {job_id} exception:")


def recover_stuck_jobs():
    """On startup, mark any jobs stuck in 'running' as 'error'."""
    try:
        r = job_store.get_redis()
        # Scan for running jobs (best effort)
        for key in r.scan_iter(match='job:*', count=100):
            status = r.hget(key, 'status')
            if status == 'running':
                job_id = key.split(':')[1]
                log.warning(f"Recovering stuck job {job_id} (marking as error)")
                job_store.update_job(job_id, status='error')
                job_store.publish_log(job_id, 'error', 'Job interrupted by worker restart. Please retry.')
    except Exception as e:
        log.warning(f"Could not recover stuck jobs: {e}")


def main():
    log.info(f'Worker starting (max_concurrent={MAX_CONCURRENT}, results_dir={RESULTS_DIR})')
    log.info(f'Engine: shared-browser (1 Chromium process, many contexts)')
    log.info(f'Redis: {job_store.REDIS_URL}')

    # Wait for Redis
    for attempt in range(30):
        if job_store.ping():
            log.info('Redis connected')
            break
        log.info(f'Waiting for Redis... (attempt {attempt + 1})')
        time.sleep(2)
    else:
        log.error('Could not connect to Redis, exiting')
        sys.exit(1)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    recover_stuck_jobs()

    while not shutdown_requested:
        try:
            r = job_store.get_redis()
            result = r.brpop('job_queue', timeout=POLL_INTERVAL)

            if result is None:
                continue

            _, job_id = result
            log.info(f'Picked up job: {job_id}')
            asyncio.run(process_job(job_id))

        except KeyboardInterrupt:
            break
        except (ConnectionError, TimeoutError) as e:
            log.warning(f'Redis connection lost: {e}, reconnecting...')
            job_store.reset_redis()
            time.sleep(5)
        except Exception as e:
            log.error(f'Error in worker loop: {e}')
            time.sleep(5)

    log.info('Worker shutting down')


if __name__ == '__main__':
    main()
