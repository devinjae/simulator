from fastapi import APIRouter, Depends
from app.dependencies import get_news_engine

router = APIRouter()

@router.post("/news")
async def create_news(news_engine = Depends(get_news_engine)):
    
    return {"message": "News created successfully"}
