from fastapi import FastAPI
from app.routes import user # Importe o arquivo de rotas

app = FastAPI(title="Stella Vita API")

# Inclui as rotas de usuários
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Stella Vita API is running"}