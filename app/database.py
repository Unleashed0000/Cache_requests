import redis
import json
from config import redis_host, redis_port


class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0, decode_responses=True):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=decode_responses)

    def get_from_cache(self, key):
        cached_response = self.redis_client.get(key)
        return json.loads(cached_response) if cached_response else None

    def set_to_cache(self, key, value, expiration_time=3600):
        self.redis_client.setex(key, expiration_time, json.dumps(value))

    def get(self, key):
        value =  self.redis_client.get(key)
        return [] if value == "null" else json.loads(value)
    def exists_in_database(self, key):
        return self.redis_client.exists(key)

    def associate_url_with_cache_key(self, url, cache_key):
        # Используем lpush для добавления значения в начало списка
        self.redis_client.lpush(url, cache_key)

    def get_cache_key_for_url(self, url):
        # Используем lrange для получения всех значений из списка
        return self.redis_client.lrange(url, 0, -1)
    def delete_cache_for_url(self, url):
        # Используем del для удаления ключа и связанных с ним значений
        self.redis_client.delete(url)
    def set(self, key, value):
        # Сериализуем список в строку JSON перед сохранением в Redis
        serialized_value = json.dumps(value)
        self.redis_client.set(key, serialized_value)
    def clear(self):
        self.redis_client.flushdb()


# Создание объекта RedisCache
redis_cache = RedisCache()