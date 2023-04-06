from fastapi.staticfiles import StaticFiles
from api.endpoints import home, issue
from api.app import app


app.mount("/static", StaticFiles(directory="src/web/static"), name="static")

app.include_router(home.router)
app.include_router(issue.router)
