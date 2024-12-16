from app.database import neo4j_conn
from app.schemas.user import ChapterRelationCreate, ChapterRelationResponse


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
def process_relation_data(raw_data):
    """
    将原始数据处理为符合 ChapterRelationResponse 的格式
    """
    processed_data = {
        "start_chapter": raw_data["start_properties"]["name"],  # 提取起始章节的名称
        "start_labels": raw_data["start_labels"],
        "start_properties": raw_data["start_properties"],

        "relation": raw_data["relation"],
        "relation_properties": raw_data["relation_properties"],

        "end_chapter": raw_data["end_properties"]["name"],  # 提取终止章节的名称
        "end_labels": raw_data["end_labels"],
        "end_properties": raw_data["end_properties"],
    }
    return ChapterRelationResponse(**processed_data)


def get_graph_relations():
    """
    查询知识图谱中的所有节点及关系的详细信息
    :return: 列表，每一项为 ChapterRelationResponse 对象
    """
    query = """
    MATCH (start)-[r]->(end)
    RETURN 
        start.id AS start_id, 
        labels(start) AS start_labels, 
        properties(start) AS start_properties, 
        TYPE(r) AS relation, 
        properties(r) AS relation_properties, 
        end.id AS end_id, 
        labels(end) AS end_labels, 
        properties(end) AS end_properties
    """
    with neo4j_conn.get_session() as session:
        result = session.run(query)
        records = result.data()

        responses = []
        for record in records:
            response = ChapterRelationResponse(
                start_id=record["start_id"],
                start_labels=record["start_labels"],
                start_properties=record["start_properties"],

                relation=record["relation"],
                relation_properties=record["relation_properties"],

                end_id=record["end_id"],
                end_labels=record["end_labels"],
                end_properties=record["end_properties"]
            )
            responses.append(response)

        return responses