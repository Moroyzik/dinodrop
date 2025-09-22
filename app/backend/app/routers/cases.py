import math
from typing import Any, Dict, List

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.services.fair import hmac_roll


router = APIRouter()


def _get_seeds(request: Request) -> Dict[str, Any]:
    return getattr(request.app.state, "seeds", {})


@router.get("/cases")
async def list_cases(request: Request):
    seeds = _get_seeds(request)
    return {"cases": seeds.get("cases", [])}


class OpenCaseResponse(BaseModel):
    item: Dict[str, Any]
    pf: Dict[str, Any]


def _select_by_roll(items: List[Dict[str, Any]], roll: float) -> Dict[str, Any]:
    weights = [max(0.0, float(i.get("weight_dyn", i.get("weight_base", 0)))) for i in items]
    total = sum(weights) or 1.0
    target = roll * total
    acc = 0.0
    for item, w in zip(items, weights):
        acc += w
        if target <= acc:
            return item
    return items[-1]


@router.post("/cases/{case_id}/open", response_model=OpenCaseResponse)
async def open_case(case_id: int, request: Request):
    seeds = _get_seeds(request)
    s = getattr(request.app.state, "pf_session", None)
    if s is None:
        from app.services.fair import generate_pf_session

        s = generate_pf_session()
        request.app.state.pf_session = s

    roll = hmac_roll(s.server_seed, s.client_seed, s.nonce)
    s.nonce += 1

    items = [i for i in seeds.get("case_items", []) if int(i.get("case_id", 0)) == int(case_id)]
    if not items:
        return OpenCaseResponse(item={}, pf={"serverSeedHash": s.server_seed_hash, "clientSeed": s.client_seed, "nonce": s.nonce - 1, "roll": roll})
    selected = _select_by_roll(items, roll)
    return OpenCaseResponse(
        item=selected,
        pf={
            "serverSeedHash": s.server_seed_hash,
            "clientSeed": s.client_seed,
            "nonce": s.nonce - 1,
            "roll": roll,
        },
    )

