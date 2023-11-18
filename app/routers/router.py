from fastapi import APIRouter
from models import Item
import aioredis

router = APIRouter()


@router.post("/items/")
async def create_item(item: Item):
    redis = aioredis.from_url("redis://localhost")
    await redis.set(item.key, item.value)
    value = await redis.get(item.key)
    return {"message": f"Item: {value} created successfully"}