from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    SECRET: str = "69-isert-a-secret-here-420"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    authjwt_secret_key: str = SECRET
    authjwt_token_location: set[str] = {"cookies"}
    
    STATIC_URL: str = "/static"
    
    PAY_LINK_ISSUE: str = "/pay"

    DATABASE_URL: str = "pgsql://postgres:postgres@localhost:5432/autocoder"
    
    GITHUB_ACCESS_TOKEN: str = "insert-a-github-access-token-here"


settings = Settings()
