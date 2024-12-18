import logging
from typing import List

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



def get_graph_relations():
    """
    查询知识图谱中的所有节点及关系的详细信息
    :return: 列表，每一项为 ChapterRelationResponse 对象
    """
    query = """
    MATCH (start)-[r]->(end)
    RETURN 
        properties(start) AS start_properties, 
        labels(start) AS start_labels,
        TYPE(r) AS relation, 
        properties(end) AS end_properties,
        labels(end) AS end_labels
    """
    with neo4j_conn.get_session() as session:
        result = session.run(query)
        records = result.data()

        responses = []
        for record in records:
            response = ChapterRelationResponse(
                # start_id=record["start_id"],
                start_labels=record["start_labels"],
                start_properties=record["start_properties"],
                relation=record["relation"],
                # relation_properties=record["relation_properties"],
                #
                # end_id=record["end_id"],
                end_labels=record["end_labels"],
                end_properties=record["end_properties"]
            )
            responses.append(response)

        return responses


def search_chapters(search_term: str) -> List[ChapterRelationResponse]:
    """
    根据搜索关键字模糊查询章节及其相关章节
    :param search_term: 搜索关键字
    :return: 列表，每一项为 ChapterRelationResponse 对象
    """
    # 使用参数化查询以防止Cypher注入
    query = """
    MATCH (start)-[r]->(end)
    WHERE toLower(start.name) CONTAINS toLower($search_term)
    RETURN 
        properties(start) AS start_properties,
        labels(start) AS start_labels,
        TYPE(r) AS relation, 
        properties(end) AS end_properties,
        labels(end) AS end_labels
    """
    try:
        with neo4j_conn.get_session() as session:
            result = session.run(query, parameters={"search_term": search_term})
            records = result.data()

            responses = [
                ChapterRelationResponse(
                    start_labels=record.get("start_labels", []),
                    start_properties=record.get("start_properties", {}),
                    relation=record.get("relation", ""),
                    end_labels=record.get("end_labels", []),
                    end_properties=record.get("end_properties", {}),
                )
                for record in records
            ]

            return responses
    except Exception as e:
        logging.error(f"Error during search_chapters: {e}")
        return []