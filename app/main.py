
from fastapi import FastAPI
from app.routers import user, subscription, fund
from app.utils.database import connect_db

app = FastAPI()

# Conectar a la base de datos
connect_db()

# Incluir routers
app.include_router(fund.router)
app.include_router(user.router)
app.include_router(subscription.router)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Fondos de Inversión"}
