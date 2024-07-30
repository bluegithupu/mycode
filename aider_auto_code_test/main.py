from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get("/print")
def print_endpoint():
    return "it is my print"


