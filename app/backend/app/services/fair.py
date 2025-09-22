import hashlib
import hmac
import os
import struct
from dataclasses import dataclass


def hmac_roll(server_seed: str, client_seed: str, nonce: int) -> float:
    message = f"{client_seed}:{nonce}".encode()
    digest = hmac.new(server_seed.encode(), message, hashlib.sha256).digest()
    number = struct.unpack(">Q", digest[:8])[0]
    return number / 2 ** 64


def sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


@dataclass
class ProvablyFairSession:
    server_seed: str
    server_seed_hash: str
    client_seed: str
    nonce: int


def generate_pf_session(client_seed: str | None = None, nonce: int = 0) -> ProvablyFairSession:
    server_seed = os.urandom(32).hex()
    client_seed_final = client_seed or os.urandom(8).hex()
    return ProvablyFairSession(
        server_seed=server_seed,
        server_seed_hash=sha256_hex(server_seed),
        client_seed=client_seed_final,
        nonce=nonce,
    )

