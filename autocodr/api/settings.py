from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    SECRET: str = "69-isert-a-secret-here-420"

    authjwt_secret_key: str = SECRET
    authjwt_token_location: set = {"cookies"}

    DATABASE_URL: str = "pgsql://postgres:postgres@localhost:5432/autocoder"
