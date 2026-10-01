from fastapi import FastAPI
from api.routers import chat_endpoint

app = FastAPI()

app.include_router(chat_endpoint.router, prefix="/api")

@app.get('/health')
async def health():
    return {"status": "healthy"}
