import os
import rq
import redis

# run queued jobs od 'default' queue
if __name__ == '__main__':
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    conn = redis.from_url(redis_url)
    with rq.Connection(conn):
        worker = rq.Worker(rq.Queue('default'))
        worker.work()