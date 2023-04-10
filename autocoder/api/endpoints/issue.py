from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from autocoder.database.models import Issue

router = APIRouter()

class IssueCreate(BaseModel):
    """ Create an issue """
    issue_url: str
    access_token: str | None


@router.post("/api/issue/create")
async def create_issue(issue: IssueCreate):
    """ Create an issue in the database """
    try:
        Issue.from_url(
            issue_url = issue.issue_url, 
            access_token = issue.access_token or None
            )
        return JSONResponse(
            status_code=200, 
            content={"status": "ok"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=400, 
            content={
                "status": "error", 
                "message": str(e)
            })