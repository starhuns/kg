from app.database import neo4j_conn
from app.schemas.user import ChapterRelationCreate

def create_chapter_relation(relation_data: ChapterRelationCreate):
    """
    创建章节关系
    :param relation_data: 包含起始章节、结束章节和关系类型
    :return: 创建的关系数据
    """
    query = """
    MERGE (start:Chapter {name: $start_chapter})
    MERGE (end:Chapter {name: $end_chapter})
    CREATE (start)-[r:%s]->(end)
    RETURN start.name AS start_chapter, TYPE(r) AS relation, end.name AS end_chapter
    """ % relation_data.relation.upper()  # 使用动态关系类型

    # 获取 session 进行查询
    with neo4j_conn.get_session() as session:
        result = session.run(query, parameters={
            "start_chapter": relation_data.start_chapter,
            "end_chapter": relation_data.end_chapter,
        })
        record = result.single()
        return {
            "start_chapter": record["start_chapter"],
            "relation": record["relation"],
            "end_chapter": record["end_chapter"],
        }

def get_chapter_relations():
    """
    查询所有章节关系
    :return: 列表，包含所有章节关系数据
    """
    query = """
    MATCH (start:Chapter)-[r]->(end:Chapter)
    RETURN start.name AS start_chapter, TYPE(r) AS relation, end.name AS end_chapter
    """
    with neo4j_conn.get_session() as session:
        result = session.run(query)
        records = result.data()  # 将 Result 对象转为列表
        return [
            {
                "start_chapter": record["start_chapter"],
                "relation": record["relation"],
                "end_chapter": record["end_chapter"],
            }
            for record in records
        ]
