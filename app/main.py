import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import user
from app.database import neo4j_conn

app = FastAPI()

# 注册用户路由
app.include_router(user.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，可以设置特定域名，如 ["http://localhost:3000"]
    allow_credentials=True,  # 支持发送 cookies
    allow_methods=["*"],  # 允许所有方法，例如 ["GET", "POST"]
    allow_headers=["*"],  # 允许所有请求头
)

@app.get("/")
def read_root():
    return {"message": "FastAPI with Neo4j"}
if __name__=='__main__':
    uvicorn.run('main:app',host='127.0.0.1',port=8000,reload=True)