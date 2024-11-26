from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    neo4j_uri: str = "bolt://localhost:7687"  # 替换为你的 Neo4j 地址
    neo4j_user: str = "neo4j"                # 替换为你的用户名
    neo4j_password: str = "12345678"         # 替换为你的密码

    class Config:
        env_file = ".env"

settings = Settings()
