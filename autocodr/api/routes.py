from autocodr.api import app
from autocodr.api.endpoints import home, healthcheck, login


app.include_router(home.router)
app.include_router(healthcheck.router)
app.include_router(login.router, prefix="/api")
