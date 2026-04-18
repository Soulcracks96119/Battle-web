from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import os
import random
from typing import Optional
from datetime import datetime

app = FastAPI(title="Bot API", description="API for Telegram Bot", version="1.0.0")

# CORS allow kar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 API Key - Railway Variables se lega
VALID_API_KEY = os.environ.get("API_KEY", "default-key-change-me")

# Key verify karne ka function
def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key missing! Please provide X-API-Key header")
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key!")
    return True

# ============ PUBLIC ROUTES (Bina Key Ke) ============

@app.get("/")
def home():
    return {
        "message": "🚀 Bot API is live on Railway!",
        "status": "online",
        "endpoints": {
            "public": ["/", "/health", "/api/v1/health"],
            "protected": ["/hello/{name}", "/random-number", "/add", "/joke", "/stats"]
        }
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "uptime": "running smoothly",
        "timestamp": datetime.now().isoformat()
    }

# ✅ Bot ke liye special endpoint (wahi jo bot dhundh raha tha)
@app.get("/api/v1/health")
def api_v1_health():
    return {
        "status": "healthy",
        "message": "API is working perfectly",
        "version": "v1",
        "timestamp": datetime.now().isoformat()
    }

# ============ PROTECTED ROUTES (Key Chahiye) ============

@app.get("/hello/{name}")
def hello(name: str, auth: bool = Depends(verify_api_key)):
    return {"message": f"Hello {name}! Welcome to Bot API"}

@app.get("/random-number")
def random_number(auth: bool = Depends(verify_api_key)):
    return {"random": random.randint(1, 1000)}

@app.get("/add")
def add(a: int, b: int, auth: bool = Depends(verify_api_key)):
    return {"result": a + b}

@app.get("/joke")
def joke(auth: bool = Depends(verify_api_key)):
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the developer go broke? Because he used up all his cache!",
        "What is a programmer's favorite place? The Foo Bar!",
        "Why do Java developers wear glasses? Because they can't C#!"
    ]
    return {"joke": random.choice(jokes)}

@app.get("/stats")
def stats(auth: bool = Depends(verify_api_key)):
    return {
        "total_requests": random.randint(1000, 9999),
        "active_users": random.randint(10, 100),
        "uptime_percentage": 99.9,
        "status": "operational"
    }

# Bot running attacks ke liye (agar bot yeh dhundh raha hai)
@app.get("/running")
def running(auth: bool = Depends(verify_api_key)):
    return {"attacks": [], "message": "No active attacks"}

# Bot users list ke liye
@app.get("/users")
def users(auth: bool = Depends(verify_api_key)):
    return {"users": [], "total": 0}

# Bot statistics ke liye
@app.get("/stats/bot")
def bot_stats(auth: bool = Depends(verify_api_key)):
    return {
        "total_users": 0,
        "approved_users": 0,
        "total_attacks": 0,
        "system_health": "good"
    }
