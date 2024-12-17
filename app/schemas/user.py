from pydantic import BaseModel
from typing import Dict, List, Optional


# 定义关系创建模型
class ChapterRelationCreate(BaseModel):
    start_chapter: str  # 起始章节的名称
    end_chapter: str  # 终止章节的名称
    relation: str  # 关系类型（如 "FOLLOWS", "RELATED_TO" 等）


# 定义关系查询响应模型
class ChapterRelationResponse(BaseModel):
    # start_id: str
    start_labels: List[str]
    start_properties: Dict

    relation: str
    # relation_properties: Dict
    #
    # end_id: str
    end_labels: List[str]
    end_properties: Dict

