from fastapi import APIRouter

router = APIRouter()

@router.post("/news")
async def create_news():
    return {"message": "News created successfully"}
