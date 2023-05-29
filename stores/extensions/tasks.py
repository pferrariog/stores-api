from flask import Flask
from redis import Redis
from rq.queue import Queue


def init_app(app: Flask) -> None:
    """Redis queues configuration"""
    connection = Redis.from_url(app.config.get("REDIS_URL"))
    app.queue = Queue("email_sender", connection=connection)
