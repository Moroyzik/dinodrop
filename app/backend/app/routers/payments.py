from fastapi import APIRouter
from pydantic import BaseModel

from app.services.providers import get_crypto_client, get_yookassa_client


router = APIRouter(prefix="/payments")


class DepositYooKassaRequest(BaseModel):
    amount_rub: int


@router.post("/deposit/yookassa")
async def deposit_yookassa(body: DepositYooKassaRequest):
    client = get_yookassa_client()
    res = await client.create_payment(body.amount_rub * 100, "Deposit", "http://localhost/return")
    return {"payment_url": res.confirmation_url, "provider_id": res.provider_id}


class USDTAddressRequest(BaseModel):
    network: str


@router.post("/deposit/usdt/address")
async def deposit_usdt_address(body: USDTAddressRequest):
    client = get_crypto_client()
    addr = await client.get_deposit_address(body.network)
    return {"address": addr.address, "network": addr.network}

