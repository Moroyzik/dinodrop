import os


ENV = os.getenv("ENV", "development")
PROVIDERS_MODE = os.getenv("PROVIDERS_MODE", "mock")

SECRET_KEY = os.getenv("SECRET_KEY", "mock_secret_key")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://app:app@postgres:5432/app",
)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# External providers
STEAM_API_KEY = os.getenv("STEAM_API_KEY", "mock_steam_key")
STEAM_OPENID_RETURN = os.getenv(
    "STEAM_OPENID_RETURN", "http://localhost/auth/steam/callback"
)

YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID", "mock_shop_id")
YOOKASSA_SECRET = os.getenv("YOOKASSA_SECRET", "mock_secret")
YOOKASSA_PAYOUT_KEY = os.getenv("YOOKASSA_PAYOUT_KEY", "mock_payout")

USDT_PROVIDER_KEY = os.getenv("USDT_PROVIDER_KEY", "mock_usdt_key")
USDT_TRON_WALLET = os.getenv("USDT_TRON_WALLET", "TR_mock_wallet")
USDT_ETH_WALLET = os.getenv("USDT_ETH_WALLET", "0xmockwallet")

SMTP_HOST = os.getenv("SMTP_HOST", "mock_smtp")
SMTP_USER = os.getenv("SMTP_USER", "mock_user")
SMTP_PASS = os.getenv("SMTP_PASS", "mock_pass")
SENTRY_DSN = os.getenv("SENTRY_DSN", "mock_sentry")


def _is_mock_value(value: str) -> bool:
    return value.startswith("mock_") or value in {"mock", "dummy", "test"}


IS_MOCK = PROVIDERS_MODE == "mock" or any(
    _is_mock_value(v)
    for v in [STEAM_API_KEY, YOOKASSA_SECRET, USDT_PROVIDER_KEY]
)

if ENV == "production" and IS_MOCK:
    raise RuntimeError("Refusing to run in production with mock providers enabled")

