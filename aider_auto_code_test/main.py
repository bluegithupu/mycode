from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
def health_check():
    return "ok"

@app.get("/print")
def print_endpoint():
    return "it is my print"


