import uvicorn
from fastapi import FastAPI
from app.routers import user
from app.database import neo4j_conn

app = FastAPI()

# 注册用户路由
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "FastAPI with Neo4j"}
if __name__=='__main__':
    uvicorn.run('main:app',host='127.0.0.1',port=8000,reload=True)