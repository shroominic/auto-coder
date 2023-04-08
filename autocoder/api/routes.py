from fastapi.staticfiles import StaticFiles
from autocoder.api.endpoints import home, issue, healthcheck
from autocoder.api.app import app


app.mount("/static", StaticFiles(directory="autocoder/api/static"), name="static")

app.include_router(home.router)
app.include_router(healthcheck.router)
# app.include_router(issue.router)
