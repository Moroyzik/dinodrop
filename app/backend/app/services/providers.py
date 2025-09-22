from dataclasses import dataclass
from typing import Any, Dict

from app.config import IS_MOCK


# Steam


class RealSteamClient:
    def get_inventory(self, steam_id: str) -> Dict[str, Any]:  # pragma: no cover
        raise NotImplementedError


class MockSteamClient:
    def get_inventory(self, steam_id: str) -> Dict[str, Any]:
        return {
            "steam_id": steam_id,
            "items": [
                {"classid": "123", "name": "Field-tested AK", "price_minor": 12000},
                {"classid": "124", "name": "AWP Redline", "price_minor": 45000},
            ],
        }


# YooKassa


@dataclass
class PaymentResult:
    confirmation_url: str
    provider_id: str


class RealYooKassa:  # pragma: no cover
    async def create_payment(self, amount_minor: int, description: str, return_url: str) -> PaymentResult:
        raise NotImplementedError


class MockYooKassa:
    async def create_payment(self, amount_minor: int, description: str, return_url: str) -> PaymentResult:
        return PaymentResult(
            confirmation_url="https://mock.yookassa/confirm?id=payment_mock_123",
            provider_id="payment_mock_123",
        )


# Crypto (USDT)


@dataclass
class CryptoDepositAddress:
    address: str
    network: str


class RealCrypto:  # pragma: no cover
    async def get_deposit_address(self, network: str) -> CryptoDepositAddress:
        raise NotImplementedError


class MockCrypto:
    async def get_deposit_address(self, network: str) -> CryptoDepositAddress:
        return CryptoDepositAddress(address=f"mock_{network}_address_123", network=network)


def get_steam_client():
    return MockSteamClient() if IS_MOCK else RealSteamClient()


def get_yookassa_client():
    return MockYooKassa() if IS_MOCK else RealYooKassa()


def get_crypto_client():
    return MockCrypto() if IS_MOCK else RealCrypto()

