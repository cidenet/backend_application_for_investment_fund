
from fastapi import FastAPI
from app.routers import user, subscription, fund
from fastapi.middleware.cors import CORSMiddleware
from app.utils.database import connect_db

app = FastAPI()

# Connect to the database
connect_db()

# Configure CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(fund.router)
app.include_router(user.router)
app.include_router(subscription.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Investment Funds API"
    }
