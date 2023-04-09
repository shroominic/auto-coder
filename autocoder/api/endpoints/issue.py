from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from autocoder.database.models import Issue

router = APIRouter()


@router.post("/api/issue/create")
def create_issue(request: Request):
    """ Create an issue in the database """
    Issue.from_url(
        url          = request.json().get("issue_url"), 
        access_token = request.json().get("access_token")
    )
    
    return JSONResponse(
        status_code=200, 
        content={"message": "Issue created"}
    )