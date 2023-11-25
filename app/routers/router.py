from fastapi import APIRouter, Request, HTTPException
from models import AllRequestPost, AllInitialPost, RequestDelete
from database import redis_cache
from request_handler import handle_request, make_request
from server_imitation import imitate

router = APIRouter()


@router.post("/post")
async def post(request: AllRequestPost):
   """Добавить описание"""

   await handle_request('POST', request)


@router.put("/put")
async def put(request: Request):
   """Добавить описание"""
   try:
      headers = dict(request.headers)
      data_xml = await request.body()
      
      # Здесь вы можете использовать headers и data_xml по своему усмотрению
      print(headers)
      print(data_xml)
      return {"status": "success"}
   except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))
   #await func("PUT",request)


@router.post("/post/initial")
async def post(request: AllInitialPost):
   """Добавляем payin идентификатор, по которому потом сможем удалить закешированные запросы"""
   print(request.use_exclude_columns)
   if request.database =='Redis':
      redis_cache.set('url_ext', request.url_ext)
      redis_cache.set('exclude_columns', request.exclude_columns)
      redis_cache.set('key_columns', request.key_columns)
      redis_cache.set('use_exclude_columns', request.use_exclude_columns)
      redis_cache.set('headers', request.headers)


@router.delete("/delete")
async def delete(request: RequestDelete):
    if request.database =='Redis':
        cached_response = redis_cache.get_cache_key_for_url(request.url_ext)
        print('КЭШ ДЛЯ НАШЕГО URL=',cached_response)
        print('ALLLLL= ',len(cached_response))    
        for cache in cached_response:
           redis_cache.delete_cache_for_url(cache)
        redis_cache.delete_cache_for_url(request.url_ext)


@router.get("/get")
async def get(request: Request):
    query_params = dict(request.query_params)
    print(query_params)
    if query_params['database']=='Redis':
        headers = redis_cache.get('headers')
        url_ext = redis_cache.get('url_ext')
        # Your code here
        #print(params['url_ext'])
        #print(request.headers)
        response = make_request(url_ext, 'GET', headers)
        print(response)    

@router.get("/test")
def test():
   """Имитация payin запросов"""
   
   imitate()
