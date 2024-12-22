'''
Author: hushuhan 873933169@qq.com
Date: 2024-12-10 23:03:36
LastEditors: hushuhan 873933169@qq.com
LastEditTime: 2024-12-16 23:50:41
FilePath: \FavorSystem\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from fastapi import FastAPI
from fastapi import Form, File, UploadFile
from fastapi import Header, Cookie, Query, Depends
from fastapi import HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from people import people_api

app = FastAPI()

app.mount("/people", people_api)

# 设置允许的源
origins = [
    "http://example.com",
    "https://example.com",
    "http://localhost",
    "http://localhost:8080",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的方法
    allow_headers=["*"],  # 允许的头
)

class Item(BaseModel):
    name: str = Field(..., title="Item Name", max_length=100)
    description: str = Field(None, title="Item Description", max_length=255)
    price: float = Field(..., title="Item Price", gt=0)

@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}

# 路由操作函数
@app.post("/files/")
async def create_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

# 依赖项函数1
def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# 依赖项函数2
def verify_token(token: str = Depends(common_parameters)):
    if token is None:
        raise HTTPException(status_code=400, detail="Token required")
    return token

# 路由操作函数
@app.get("/depends/")
async def depends(commons: dict = Depends(verify_token)):
    return commons

# 后处理函数
async def after_request():
    # 这里可以执行一些后处理逻辑，比如记录日志
    pass

# 后处理依赖项
@app.get("/depends/", response_model=dict)
async def after(request: dict = Depends(after_request)):
    return {"message": "Items returned successfully"}

@app.get("/")
def get_test():
    return {"Hello": "World"}


@app.get("/people/{people_id}")
def get_people(people_id: int, q: str = Query(..., max_length=10)):
    return {"people_id": people_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/create/")
def create_item(item: Item):
    return item

@app.get("/header/")
def get_header(user_agent: str = Header(None), session_token: str = Cookie(None)):
    return {"User-Agent": user_agent, "Session-Token": session_token}

@app.get("/redirect")
def redirect():
    return RedirectResponse(url="/items/")

@app.get("/custom_header/{item_id}")
def custom_header(item_id: int):
    content = {"item_id": item_id}
    headers = {"X-Custom-Header": "custom-header-value"}
    return JSONResponse(content=content, headers=headers)
