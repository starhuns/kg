from fastapi import APIRouter
from typing import List

from app.schemas.user import ChapterRelationCreate, ChapterRelationResponse
from app.services.user_service import create_chapter_relation, get_chapter_relations

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
    return get_chapter_relations()
