from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/healthcheck/", response_class=JSONResponse)
async def healthcheck(request: Request):
    """ Return {"status": "ok"} if all right """
    return {"status": "ok"}