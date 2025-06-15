import time
from fastapi import HTTPException, Request

# Memory rate limiter (simple IP-based, per 60 sec)
rate_limit_store = {}


def check_rate_limit(request: Request, max_requests: int = 10):
    ip = request.client.host
    now = time.time()
    window = 60  # seconds

    if ip not in rate_limit_store:
        rate_limit_store[ip] = []

    rate_limit_store[ip] = [t for t in rate_limit_store[ip] if now - t < window]

    if len(rate_limit_store[ip]) >= max_requests:
        raise HTTPException(429, detail="Rate limit exceeded. Max 10 requests per minute.")

    rate_limit_store[ip].append(now)
