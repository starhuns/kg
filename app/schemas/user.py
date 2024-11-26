from pydantic import BaseModel


# 定义关系创建模型
class ChapterRelationCreate(BaseModel):
    start_chapter: str  # 起始章节的名称
    end_chapter: str    # 终止章节的名称
    relation: str       # 关系类型（如 "FOLLOWS", "RELATED_TO" 等）

# 定义关系查询响应模型
class ChapterRelationResponse(BaseModel):
    start_chapter: str
    end_chapter: str
    relation: str
