import os

import redis
import rq

import backend.dev_settings

import backend.user_impl


class Tasker(object):

    def __init__(self, env=None):
        if env is None:
            env = os.environ.get("APP_ENV", "dev")
        self.settings = {
            "dev": backend.dev_settings,
        }[env]

        self.redis: redis.Redis = redis.StrictRedis(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            db=self.settings.REDIS_DB)
        self.task_queue: rq.Queue = rq.Queue(
            name=self.settings.TASK_QUEUE_NAME,
            connection=self.redis)