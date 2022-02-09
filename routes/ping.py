###for testing purposes only

from fastapi import APIRouter
router = APIRouter(tags=['ping'])
@router.get("/ping")
async def pong():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}