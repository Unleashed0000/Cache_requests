from fastapi import FastAPI
from routers.router import router as api_router
import uvicorn

app = FastAPI()

app.include_router(api_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")