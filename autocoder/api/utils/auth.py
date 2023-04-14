from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT, exceptions
from autocoder.database.models import User
from autocoder.database.utils import get
from ..core import Settings


@AuthJWT.load_config
def get_config():
    return Settings()


async def authenticate_user(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        decoded_token = authorize.get_raw_jwt()
        user = await get(User, email=decoded_token["sub"])
        return user
    except exceptions.AuthJWTException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))