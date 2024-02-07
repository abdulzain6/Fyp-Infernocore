import redis
import logging

class TargetStatusManager:
    def __init__(self, client: redis.Redis):
        self.redis_client = client
        self.online_targets_set = 'online_targets'

    def mark_target_online(self, target_id: str):
        logging.info(f"Marking {target_id} online.")
        self.redis_client.sadd(self.online_targets_set, target_id)

    def mark_target_offline(self, target_id: str):
        logging.info(f"Marking {target_id} offline.")
        self.redis_client.srem(self.online_targets_set, target_id)

    def is_target_online(self, target_id: str) -> bool:
        return self.redis_client.sismember(self.online_targets_set, target_id)

    def get_online_targets(self) -> list:
        data = list(self.redis_client.smembers(self.online_targets_set))
        logging.info(f"Getting online targets list {data}")
        return [str(d) for d in data]
