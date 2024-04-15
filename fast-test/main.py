from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Cookie(BaseModel):
    key: str
    value: str

@app.get("/get-all-cookie", response_model=dict)
def get_all_cookies(request: Request):
    print("in ------------")
    cookies = request.cookies
    print(cookies)

    # all_cookies = {cookie_name: cookie_value for cookie_name, cookie_value in cookies.items()}
    return cookies