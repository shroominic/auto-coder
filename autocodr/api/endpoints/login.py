import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, APIRouter
from fastapi_jwt_auth import AuthJWT  # type: ignore
from sqlmodel.ext.asyncio.session import AsyncSession

from autocodr.database import get_session, models
from autocodr.api.utils.email import send_login_email
from autocodr.api.utils.auth import authenticate_user


router = APIRouter()


@router.post("/request-login")
async def request_email_link(email: str, session: AsyncSession = Depends(get_session)):
    try:  
        user = await models.User.from_email(session, email)
        # create token
        # user.login_token = str(uuid.uuid4())
        # user.token_expiration = datetime.now() + timedelta(minutes=15)
        await user.update_login_token(session)

        await send_login_email(user, user.login_token)
        return {
            "status": "ok", 
            "message": f"Email sent to {email}."
        }

    except Exception as e:
        print(e)
        return {
            "status": "error", 
            "message": str(e)
        }


@router.get("/login")
async def login(token: str, session: AsyncSession = Depends(get_session)):
    user = (await session.execute(select(models.User).filter_by(login_token=token))).scalar_one_or_none()
    if not user: raise HTTPException(status_code=400, detail="Invalid login token")
    else: print(user.email, user.login_token, user.token_expiration)
    if not user.token_is_valid(): raise HTTPException(status_code=400, detail="Login token expired")
    
    # Invalidate the token after use
    user.login_token = None
    user.token_expiration = None
    await session.commit()

    access_token = AuthJWT().create_access_token(subject=user.email, expires_time=timedelta(days=30))
    return {"email": user.email, "access_token": access_token}


@router.get("/auth-test")
async def protected_route(user: User = Depends(authenticate_user)):
    return {"message": f"Hello, {user.email}!"}
