from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter
from .core import app
from .endpoints import home, healthcheck, issue, login


app.mount("/static", StaticFiles(directory="autocoder/api/static"), name="static")

app.include_router(home.router)
app.include_router(healthcheck.router)
app.include_router(issue.router, prefix="/api")
app.include_router(login.router, prefix="/api")
