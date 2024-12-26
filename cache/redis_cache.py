import redis
from typing import Optional

class RedisCache:
    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.redis_client = redis.Redis(host=host, port=port)

    def get_price(self, product_title: str) -> Optional[float]:
        price = self.redis_client.get(product_title)
        return float(price) if price else None

    def set_price(self, product_title: str, price: float) -> None:
        self.redis_client.set(product_title, str(price))