from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services.fair import ProvablyFairSession, generate_pf_session, hmac_roll, sha256_hex


router = APIRouter()

_SESSION: ProvablyFairSession | None = None


class PFSeedResponse(BaseModel):
    serverSeedHash: str
    clientSeed: str
    nonce: int


class PFSeedUpdate(BaseModel):
    clientSeed: str


def _ensure_session() -> ProvablyFairSession:
    global _SESSION
    if _SESSION is None:
        _SESSION = generate_pf_session()
    return _SESSION


@router.get("/seed", response_model=PFSeedResponse)
async def get_seed():
    s = _ensure_session()
    return PFSeedResponse(serverSeedHash=s.server_seed_hash, clientSeed=s.client_seed, nonce=s.nonce)


@router.post("/seed", response_model=PFSeedResponse)
async def set_client_seed(body: PFSeedUpdate):
    s = _ensure_session()
    s.client_seed = body.clientSeed
    s.nonce = 0
    return PFSeedResponse(serverSeedHash=s.server_seed_hash, clientSeed=s.client_seed, nonce=s.nonce)


class PFVerifyQuery(BaseModel):
    serverSeed: str
    clientSeed: str
    nonce: int
    roll: float | None = None


@router.get("/verify")
async def verify(serverSeed: str, clientSeed: str, nonce: int, roll: float | None = None):
    computed = hmac_roll(serverSeed, clientSeed, nonce)
    return {"ok": roll is None or abs(computed - roll) < 1e-18, "computed": computed, "serverSeedHash": sha256_hex(serverSeed)}

