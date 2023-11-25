from fastapi import APIRouter, Request
from models import AllRequestPost, AllInitialPost
from database import redis_cache
from request_handler import handle_request
from server_imitation import imitate

router = APIRouter()


@router.post("/post")
async def post(request: AllRequestPost):
   """Добавить описание"""

   await handle_request('POST', request)


@router.put("/put")
async def put(request: AllRequestPost):
   """Добавить описание"""

   await handle_request("PUT", request)


@router.post("/post/initial")
async def post(request: AllInitialPost):
    """Добавляем payin идентификатор, по которому потом сможем удалить закешированные запросы"""

    if request.database =='Redis':
        redis_cache.set('url_ext',request.url_ext)
        redis_cache.set('exclude_columns',request.exclude_columns)
        redis_cache.set('key_columns',request.key_columns)
        redis_cache.set('flag_columns',request.flag_columns)
        redis_cache.set('headers',request.headers)


@router.get("/get")
async def get(request: Request):
    """Добавить описание"""

    data = request.headers
    print(data)
    # Your code here
    #print(params['url_ext'])
    #print(request.headers)
    #response = make_request(params['url_ext'], 'GET',request.headers)
    #print(response)    
    #return {"url_ext": params['url_ext']}

@router.get("/test")
async def test():
   """Имитация payin запросов"""

   await imitate()
