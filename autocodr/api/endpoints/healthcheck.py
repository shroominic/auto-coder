from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/healthcheck/", response_class=JSONResponse)
async def healthcheck(request: Request):
    """ Healthcheck endpoint """
    return {"status": "ok"}