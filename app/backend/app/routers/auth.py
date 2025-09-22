from fastapi import APIRouter
from starlette.responses import RedirectResponse


router = APIRouter(prefix="/auth")


@router.get("/steam/login")
async def steam_login():
    return RedirectResponse(url="/auth/steam/callback?openid.mock=1&steam_id=7656119_mock_user")


@router.get("/steam/callback")
async def steam_callback(steam_id: str | None = None):
    return {"steam_id": steam_id or "7656119_mock_user", "token": "mock_jwt"}

