from autocodr.api import app
from autocodr.api.endpoints import healthcheck, home, login

app.include_router(home.router)
app.include_router(healthcheck.router)
app.include_router(login.router, prefix="/api")
