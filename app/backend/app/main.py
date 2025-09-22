from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.provably_fair import router as pf_router
from app.routers.cases import router as cases_router
from app.routers.auth import router as auth_router
from app.routers.payments import router as payments_router
from app.routers.me import router as me_router
from app.state import load_seeds_from_file
from app.services.fair import generate_pf_session


def create_app() -> FastAPI:
    app = FastAPI(title="DinoDrop MVP API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(pf_router, prefix="/provably-fair", tags=["provably_fair"]) 
    app.include_router(cases_router, tags=["cases"]) 
    app.include_router(auth_router, tags=["auth"]) 
    app.include_router(payments_router, tags=["payments"]) 
    app.include_router(me_router, tags=["me"]) 

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    # Load seeds into app.state
    app.state.seeds = load_seeds_from_file()
    app.state.pf_session = generate_pf_session()

    return app


app = create_app()

