import socket
import requests
import json
from databases.redis import redis_cache
from models import AllRequestPost
import xmltodict

async def handle_request(method, request: AllRequestPost):
   # print(method)
    url_ext = ''
    exclude_columns = []
    key_columns = []
    use_exclude_columns = True
    database = 'Redis' if not hasattr(request, 'database') else request.database
    if  database =='Redis':
        url_ext = redis_cache.get('url_ext')
        exclude_columns = redis_cache.get('exclude_columns')
        key_columns= redis_cache.get('key_columns')
        use_exclude_columns= redis_cache.get('use_exclude_columns')
    content_type_header = request.headers.get('Content-Type', '').lower()
    if 'json' in content_type_header:
        json_data = json.dumps(request.data)
        respons = make_request(url_ext, method,request.headers,json_data,database,exclude_columns,key_columns,use_exclude_columns)
        return respons
    elif 'xml' in content_type_header:
        print("XML data processing")
        request_body_bytes = await request.body()
        request_body_string = request_body_bytes.decode('utf-8')
        xml_dict = xmltodict.parse(request_body_string)
        xml_dict = json.dumps(xml_dict)
        respons = make_request(url_ext, method,request.headers,xml_dict,database,exclude_columns,key_columns,use_exclude_columns)
        print(respons)
        return respons
        # Добавьте обработку XML данных
    else:
        # На вход request.body() результатом является 
        print("Unsupported content type")

    return {"status": "OK"}


def make_request(url, method, headers,body={},database="Redis",exclude=[],key=[],flag = True):
    # удаляем не влияющие поля
    body_copy = {}
    if body!={}:
        if flag: # Удаление не ключевых полей:
            body_copy = json.loads(body)
            for i in exclude:
                if i in body_copy:
                    del body_copy[i]
        else: # Выбираем только ключевые поля
            body_copy = json.loads(body)
            for i in body_copy:
                if not (i in key):
                    del body_copy[i]
    if database=='Redis':
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
    


# Ф-ция для отправки сообщений, с учетом того, что может прийти коллбэк
# Логика работы:  Отправляем сообщение тест-среде через сокет, некоторое время (5сек) сокет считывает все приходящие сообщения 
# Все полученные сообщения кэшируются и записываются в базу.  Ключом является строка url
# key-callback - наборей полей по которому определяется какому именно сообщению принадлежит колл-бэк
# Сейчас ф-ция работает синхронно т.е. в один момент времени только 1 сокет открыт, поэтому поле <id> 
# не требуется для распознавания сообщения, в каждый момент сокет слушает только 1 сервер, поэтому все ответы он относит к отправленному сообщению.
# Можно сделать асинхронно, чтобы открывалось несколько сокетов сразу, и новые сообщения добавлялись только по ключевым полям.
def make_request_socket(url, method, headers,body={},database="Redis",exclude=[],key=[],flag = True,key_callback=['id']):
    # удаляем не влияющие поля
    body_copy = {}
    if body!={}:
        if flag: # Удаление не ключевых полей:
            body_copy = json.loads(body)
            for i in exclude:
                if i in body_copy:
                    del body_copy[i]
        else: # Выбираем только ключевые поля
            body_copy = json.loads(body)
            for i in body_copy:
                if not (i in key):
                    del body_copy[i]
    #key_callback_str = ','.join(key_callback)

    if database=='Redis':
        cache_callback_key = f"{url}:callback"
        # Создание уникального ключа на основе параметров запроса
        cache_key = f"{url}:{method}:{headers}:{body_copy}"

        # Проверка наличия кэша
        cached_response = redis_cache.get_from_cache(cache_key)
        # Сохранение связи между URL и ключом кэша

        # Получение ключа кэша для заданного URL
        lst_cached = []   # Тут ПОЛУЧИТЬ СПИСОК кэшей, что то аналогичное есть в ф-ции удаления:
                        # см.          cached_response = redis_cache.get_cache_key_for_url(request.url_ext)  в router.py

        if cached_response:
            print('CASHED+')
            if len(lst_cached)>1: # Если был коллбэк
                print('CALLBACK+')
                return lst_cached
            return cached_response

        # Если кэша нет, выполняем реальный запрос
        # Сохранение результата в кэше
        host = url
        port = 443 # HTTPS по умолчанию

        # Создаем сокет
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Подключаемся к серверу
        client_socket.connect((host, int(port)))

        # Преобразуем тело запроса в строку
        request_data = f"{method} / HTTP/1.1\r\n"
        request_data += f"Host: {host}\r\n"        
        for key, value in headers.items():
            request_data += f"{key}: {value}\r\n"

        request_data += "\r\n"
        request_data += f"{body}\r\n"

        # Устанавливаем таймаут для получения ответов
        client_socket.settimeout(5)
        all_message = []
        # Читаем ответы в течение 5 секунд
        while True:
            try:
                response_data = client_socket.recv(4096)
                if not response_data:
                    break
                all_message.append(response_data.decode())
            except socket.timeout:
                print("Таймаут истек. Ответы не получены.")
                break

        # Закрываем сокет
        client_socket.close()
        
        response_text = '\nCALLBACK= '.join(all_message)  
        # Структура ответа вида:
        # One message
        # CALLBACK= Two message
        redis_cache.set_to_cache(cache_key,response_text)
        redis_cache.associate_url_with_cache_key(url, cache_key)

        return response_text
    