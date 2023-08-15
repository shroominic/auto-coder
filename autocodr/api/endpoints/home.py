from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from autocodr.api import settings

router = APIRouter()
templates = Jinja2Templates(directory="autocodr/frontend/templates/")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"pay_issue_link": settings.PAY_LINK_ISSUE, "static": settings.STATIC_URL, "request": request},  # type: ignore
    )
