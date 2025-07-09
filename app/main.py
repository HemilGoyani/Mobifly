from fastapi import FastAPI
from middleware.security import check_token_valid
from app.routers import user_management
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.middleware('http')(check_token_valid)


@app.get("/")
def root():
    return "Demo-Project"


origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_management.router)