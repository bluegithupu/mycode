from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get("/print")
def print_endpoint():
    return {"message": "it is my print"}

@app.get("/hello")
def hello():
    return {"message": "hello world"}


