"""
Redis-backed job store for scrape job coordination between web and worker pods.
Replaces file-based state and in-memory Queue.
"""

import json
import logging
import os
import threading
import uuid
import time
import redis

log = logging.getLogger(__name__)

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

_redis_client = None
_redis_lock = threading.Lock()


def get_redis():
    """Get or create a thread-safe Redis client with auto-reconnect."""
    global _redis_client
    if _redis_client is None:
        with _redis_lock:
            if _redis_client is None:
                _redis_client = redis.Redis.from_url(
                    REDIS_URL,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True,
                    health_check_interval=30,
                )
    return _redis_client


def reset_redis():
    """Force reconnection on next call (used after connection failures)."""
    global _redis_client
    with _redis_lock:
        _redis_client = None


def _safe_redis_call(func, *args, default=None, **kwargs):
    """Execute a Redis call with error handling and auto-reconnect."""
    try:
        return func(*args, **kwargs)
    except (redis.ConnectionError, redis.TimeoutError) as e:
        log.warning(f"Redis connection error: {e}, reconnecting...")
        reset_redis()
        try:
            return func(*args, **kwargs)
        except Exception as e2:
            log.error(f"Redis retry failed: {e2}")
            return default
    except redis.RedisError as e:
        log.error(f"Redis error: {e}")
        return default


# --- Job Management ---

def create_job(searches, max_pages, use_proxies, concurrent, chunk_output, max_businesses, username):
    """Create a new scrape job and enqueue it. Returns job_id."""
    r = get_redis()
    job_id = str(uuid.uuid4())[:8]

    job_data = {
        'status': 'pending',
        'user': username,
        'searches': json.dumps(searches),
        'max_pages': str(max_pages),
        'use_proxies': '1' if use_proxies else '0',
        'concurrent': str(concurrent),
        'chunk_output': '1' if chunk_output else '0',
        'max_businesses': str(max_businesses),
        'total_searches': str(len(searches)),
        'completed': '0',
        'businesses_found': '0',
        'errors': '0',
        'limit_reached': '0',
        'output_files': '[]',
        'created_at': str(time.time()),
    }

    pipe = r.pipeline()
    pipe.hset(f'job:{job_id}', mapping=job_data)
    pipe.lpush('job_queue', job_id)
    pipe.sadd(f'user_jobs:{username}', job_id)
    pipe.expire(f'job:{job_id}', 86400)
    pipe.execute()

    return job_id


def get_job(job_id):
    """Get job data as a dict."""
    data = _safe_redis_call(get_redis().hgetall, f'job:{job_id}', default={})
    if not data:
        return None
    try:
        data['max_pages'] = int(data.get('max_pages', 5))
        data['concurrent'] = int(data.get('concurrent', 1))
        data['max_businesses'] = int(data.get('max_businesses', 0))
        data['total_searches'] = int(data.get('total_searches', 0))
        data['completed'] = int(data.get('completed', 0))
        data['businesses_found'] = int(data.get('businesses_found', 0))
        data['errors'] = int(data.get('errors', 0))
        data['use_proxies'] = data.get('use_proxies') == '1'
        data['chunk_output'] = data.get('chunk_output') == '1'
        data['limit_reached'] = data.get('limit_reached') == '1'
        data['searches'] = json.loads(data.get('searches', '[]'))
        data['output_files'] = json.loads(data.get('output_files', '[]'))
    except (ValueError, json.JSONDecodeError) as e:
        log.error(f"Error parsing job {job_id}: {e}")
        return None
    return data


def update_job(job_id, **kwargs):
    """Update specific fields on a job."""
    r = get_redis()
    updates = {}
    for k, v in kwargs.items():
        if isinstance(v, bool):
            updates[k] = '1' if v else '0'
        elif isinstance(v, (list, dict)):
            updates[k] = json.dumps(v)
        else:
            updates[k] = str(v)
    if updates:
        _safe_redis_call(r.hset, f'job:{job_id}', mapping=updates)


def increment_job_errors(job_id):
    """Atomically increment the error count for a job."""
    _safe_redis_call(get_redis().hincrby, f'job:{job_id}', 'errors', 1)


def stop_job(job_id):
    """Signal a job to stop."""
    _safe_redis_call(get_redis().hset, f'job:{job_id}', 'status', 'stopping')


def is_job_stopping(job_id):
    """Check if a job has been signaled to stop."""
    status = _safe_redis_call(get_redis().hget, f'job:{job_id}', 'status', default='unknown')
    return status in ('stopping', 'stopped', 'complete', 'error')


def get_user_jobs(username, limit=20):
    """Get recent jobs for a user."""
    job_ids = _safe_redis_call(get_redis().smembers, f'user_jobs:{username}', default=set())
    jobs = []
    for jid in job_ids:
        job = get_job(jid)
        if job:
            job['job_id'] = jid
            jobs.append(job)
    jobs.sort(key=lambda j: float(j.get('created_at', 0)), reverse=True)
    return jobs[:limit]


# --- Log Streaming ---

def publish_log(job_id, level, message):
    """Publish a log entry for a job (both stored and pub/sub)."""
    try:
        r = get_redis()
        entry = json.dumps({
            'level': level,
            'message': message,
            'timestamp': time.strftime('%H:%M:%S'),
        })
        pipe = r.pipeline()
        pipe.rpush(f'logs:{job_id}', entry)
        pipe.expire(f'logs:{job_id}', 86400)
        pipe.publish(f'logs_channel:{job_id}', entry)
        pipe.execute()
    except Exception as e:
        log.warning(f"Failed to publish log for {job_id}: {e}")


def get_log_history(job_id, after_index=0):
    """Get stored log entries for a job starting from an index."""
    entries = _safe_redis_call(get_redis().lrange, f'logs:{job_id}', after_index, -1, default=[])
    result = []
    for e in entries:
        try:
            result.append(json.loads(e))
        except json.JSONDecodeError:
            continue
    return result


def subscribe_logs(job_id):
    """Subscribe to live log updates for a job. Returns a pubsub object."""
    r = get_redis()
    pubsub = r.pubsub()
    pubsub.subscribe(f'logs_channel:{job_id}')
    return pubsub


# --- User Management (Redis-based, replaces SQLite) ---

def get_user(username):
    """Get user data."""
    data = _safe_redis_call(get_redis().hgetall, f'user:{username}', default={})
    if not data:
        return None
    data['is_admin'] = data.get('is_admin') == '1'
    return data


def create_user(username, password_hash, is_admin=False):
    """Create a new user."""
    r = get_redis()
    if r.exists(f'user:{username}'):
        return False
    r.hset(f'user:{username}', mapping={
        'username': username,
        'password_hash': password_hash,
        'is_admin': '1' if is_admin else '0',
        'created_at': str(time.time()),
    })
    r.sadd('users', username)
    return True


def delete_user(username):
    """Delete a user."""
    r = get_redis()
    r.delete(f'user:{username}')
    r.srem('users', username)


def list_users():
    """List all users."""
    usernames = _safe_redis_call(get_redis().smembers, 'users', default=set())
    users = []
    for uname in usernames:
        user = get_user(uname)
        if user:
            users.append(user)
    users.sort(key=lambda u: float(u.get('created_at', 0)))
    return users


def count_admins():
    """Count the number of admin users."""
    return sum(1 for u in list_users() if u.get('is_admin'))


# --- Settings ---

def get_setting(key, default=None):
    """Get an app setting."""
    val = _safe_redis_call(get_redis().hget, 'app_settings', key)
    return val if val is not None else default


def set_setting(key, value):
    """Set an app setting."""
    _safe_redis_call(get_redis().hset, 'app_settings', key, value)


# --- Health Check ---

def ping():
    """Check Redis connectivity."""
    try:
        r = get_redis()
        return r.ping()
    except Exception:
        reset_redis()
        return False
