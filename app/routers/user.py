from fastapi import APIRouter
from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.user import ChapterRelationCreate, ChapterRelationResponse
from app.services.user_service import create_chapter_relation, get_graph_relations, search_chapters

router = APIRouter(
    prefix="/chapters",
    tags=["Chapters"],
)

@router.post("/relation/", response_model=ChapterRelationResponse)
def add_chapter_relation(relation: ChapterRelationCreate):
    """
    创建章节之间的关系
    """
    return create_chapter_relation(relation)

@router.get("/relations/", response_model=List[ChapterRelationResponse])
def list_chapter_relations():
    """
    查询所有章节关系
    """
    return get_graph_relations()


@router.get("/search_chapters", response_model=List[ChapterRelationResponse])
def search_chapters_endpoint(q: str):
    """
    API 端点：根据搜索关键字模糊查询章节及其相关章节
    :param q: 搜索关键字
    :return: 匹配的章节关系列表
    """
    if not q:
        raise HTTPException(status_code=400, detail="搜索关键字不能为空")
    results = search_chapters(q)
    if not results:
        raise HTTPException(status_code=404, detail="未找到匹配的章节关系")
    return results