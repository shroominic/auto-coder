from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT, exceptions  # type: ignore

from autocodr.database.models import User

from autocodr.api.core import settings


@AuthJWT.load_config  # type: ignore
def get_config():
    return settings


async def authenticate_user(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        decoded_token = authorize.get_raw_jwt()
        user = await User.from_email(decoded_token["sub"])  # type: ignore
        return user
    except exceptions.AuthJWTException as e:
        raise HTTPException(status_code=401, detail=str(e))
