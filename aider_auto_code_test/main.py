from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
async def hello():
    return "hello world"


@app.get("/healthz")
async def healthz():
    return "ok"
