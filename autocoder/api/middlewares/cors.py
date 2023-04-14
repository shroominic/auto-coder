from fastapi.middleware.cors import CORSMiddleware
from .. import app


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins TODO: change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)