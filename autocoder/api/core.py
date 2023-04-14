from fastapi import FastAPI
from pydantic import BaseSettings


### APP ###
app = FastAPI()


### CONFIG ###
class Settings(BaseSettings):
    SECRET: str = "69-isert-a-secret-here-420"
    authjwt_secret_key: str = SECRET
