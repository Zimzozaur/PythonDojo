from fastapi import FastAPI
from asyncio import sleep

app = FastAPI()


@app.get('/')
async def read_root():
    await sleep(3)
    return {"hello": "from FastAPI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
