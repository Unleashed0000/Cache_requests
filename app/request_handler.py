import requests
import json
from database import redis_cache
from models import AllRequestPost


async def handle_request(method, request: AllRequestPost):
   # print(method)
    url_ext = ''
    exclude_columns = []
    key_columns = []
    use_exclude_columns = True
    if request.database =='Redis':
        url_ext = redis_cache.get('url_ext')
        exclude_columns = redis_cache.get('exclude_columns')
        key_columns= redis_cache.get('key_columns')
        use_exclude_columns= redis_cache.get('use_exclude_columns')

   # exclude_params = post_data.exclude_params
    #print(request.headers)
    #print(url_ext)
    #print(key_columns)
    #print(use_exclude_columns)
    #print(exclude_columns)
    content_type_header = request.headers.get('Content-Type', '').lower()
    #print(content_type_header)
    if 'json' in content_type_header:
        json_data = json.dumps(request.data)
        respons = make_request(url_ext, method,request.headers,json_data,request.database,exclude_columns,key_columns,use_exclude_columns)
       # print(response)
    elif 'xml' in content_type_header:
        print("XML data processing")
        # Добавьте обработку XML данных
    else:
        # На вход request.body() результатом является 
        print("Unsupported content type")

    return {"status": "OK"}


def make_request(url, method, headers,body={},database="Redis",exclude=[],key=[],flag = True):
    # удаляем не влияющие поля
   # print(exclude)
    body_copy = {}
    if body!={}:
        if flag: # Удаление не ключевых полей:
            body_copy = json.loads(body)
        # print(body_copy)
            for i in exclude:
                if i in body_copy:
                    del body_copy[i]
        else: # Выбираем только ключевые поля
            body_copy = json.loads(body)
            for i in body_copy:
                if not (i in key):
                    del body_copy[i]
    if database=='Redis':
       # redis_cache.clear()
        # Создание уникального ключа на основе параметров запроса
        cache_key = f"{url}:{method}:{headers}:{body_copy}"

        # Проверка наличия кэша
        cached_response = redis_cache.get_from_cache(cache_key)
        # Сохранение связи между URL и ключом кэша

        # Получение ключа кэша для заданного URL
        if cached_response:
            print('YEAH CASHED')
            return cached_response

        # Если кэша нет, выполняем реальный запрос
        # Сохранение результата в кэше
        response_text = ''
        try:
            print(headers)
            if method !='GET':
                real_response = requests.request(method, url, headers=headers, data=body)
            else:
                real_response = requests.request(method, url, headers=headers)
            response_text = "КОД="+str(real_response.status_code)+real_response.text
        except requests.exceptions.HTTPError as http_err:
            response_text = f"HTTP error occurred: {http_err}, status code: {real_response.status_code}"
        except Exception as ex:
            response_text = f"An error occurred: {ex}"
        redis_cache.set_to_cache(cache_key,response_text)
        redis_cache.associate_url_with_cache_key(url, cache_key)

        return response_text
    