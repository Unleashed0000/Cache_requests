import redis
import json

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0, decode_responses=True):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=decode_responses)

    def get_from_cache(self, key):
        cached_response = self.redis_client.get(key)
        return json.loads(cached_response) if cached_response else None

    def set_to_cache(self, key, value, expiration_time=3600):
        self.redis_client.setex(key, expiration_time, json.dumps(value))
    def clear(self):
        self.redis_client.flushdb()

# Создание объекта RedisCache
redis_cache = RedisCache()

def make_request(url, method, params,respons):
    # Создание уникального ключа на основе параметров запроса
    cache_key = f"{url}:{method}:{json.dumps(params)}"

    # Проверка наличия кэша
    cached_response = redis_cache.get_from_cache(cache_key)
   # print(cached_response)
    if cached_response:
        if 'Error' in cached_response:
            real_response = respons
            redis_cache.set_to_cache(cache_key, real_response)
            print("Была ошибка, поменяли на новый",respons)
            return respons
        else:
            print('В прошлом запросе не было ошибки, вернули результат')
        return cached_response

    # Если кэша нет, выполняем реальный запрос
    # ...

    # Сохранение результата в кэше с установленным таймаутом (в секундах)
    real_response = respons
    redis_cache.set_to_cache(cache_key, real_response)

    return real_response

redis_cache.clear()
# Пример использования
response1 = make_request('https://example.com', 'GET', {'param1': 'value1'},'OK')
print('Ответ сервера=',response1)

response2 = make_request('https://example.com', 'GET', {'param1': 'value2'},'Error')
print('Ответ сервера=',response2)
response3 = make_request('https://example.com', 'GET', {'param1': 'value2'},'Ok with warning')
print('Ответ сервера=',response3)