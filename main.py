
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "test@example.com": {
        "username": "test@example.com",
        "hashed_password": "fakehashed",
        "balance": 5000,
        "history": [],
    }
}

@app.get("/")
def read_root():
    return {"CasinoAR": "Backend funcionando"}

@app.get("/balance")
def get_balance(token: str = Depends(oauth2_scheme)):
    user = fake_users_db["test@example.com"]
    return {"balance": user["balance"]}

@app.get("/history")
def get_history(token: str = Depends(oauth2_scheme)):
    user = fake_users_db["test@example.com"]
    return user["history"]

@app.post("/play/{game}")
def play_game(game: str, amount: int, token: str = Depends(oauth2_scheme)):
    user = fake_users_db["test@example.com"]
    if amount > user["balance"]:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    user["balance"] -= amount
    result = random.choice(["Ganaste", "Perdiste"])
    if result == "Ganaste":
        user["balance"] += amount * 2
    user["history"].append(f"{game}: {result}")
    return {"juego": game, "resultado": result, "nuevo_saldo": user["balance"]}
