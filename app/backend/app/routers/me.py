from fastapi import APIRouter


router = APIRouter()


@router.get("/me")
async def me():
    return {"user_id": 2, "steam_id": "7656119_mock_user", "email": "user@example.com", "role": "user"}

