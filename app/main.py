from fastapi import FastAPI
from app.routes import user # Importe o arquivo de rotas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stella Vita API")

# Inclui as rotas de usuários
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Stella Vita API is running"}

# Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, usaremos a URL real do site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)