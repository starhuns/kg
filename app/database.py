from neo4j import GraphDatabase
from app.config import settings

class Neo4jConnection:
    def __init__(self, uri, user, password):
        # 初始化连接，只负责连接
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # 关闭连接
        self.driver.close()

    def get_session(self):
        # 提供 session 对象，供外部查询使用
        return self.driver.session()

# 初始化全局 Neo4j 连接
neo4j_conn = Neo4jConnection(
    uri=settings.neo4j_uri,
    user=settings.neo4j_user,
    password=settings.neo4j_password,
)
