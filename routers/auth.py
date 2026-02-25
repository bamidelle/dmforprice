from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from backend.database import supabase
from backend.config import settings

router = APIRouter()

# -------------------------
# Schemas
# -------------------------

class SignupRequest(BaseModel):
    email: str
    password: str
    store_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

# -------------------------
# Helpers
# -------------------------

def create_jwt(payload: dict):
    payload["exp"] = datetime.utcnow() + timedelta(days=7)
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token

def verify_jwt(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -------------------------
# Routes
# -------------------------

@router.post("/signup")
def signup(data: SignupRequest):
    # 1. Create store
    store = supabase.table("stores").insert({
        "name": data.store_name
    }).execute()

    store_id = store.data[0]["id"]

    # 2. Create user
    user = supabase.table("users").insert({
        "email": data.email,
        "password": data.password,  # hash later
        "store_id": store_id
    }).execute()

    token = create_jwt({
        "user_id": user.data[0]["id"],
        "store_id": store_id
    })

    return {
        "token": token,
        "store_id": store_id
    }

@router.post("/login")
def login(data: LoginRequest):
    user = (
        supabase.table("users")
        .select("*")
        .eq("email", data.email)
        .eq("password", data.password)
        .single()
        .execute()
    )

    if not user.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt({
        "user_id": user.data["id"],
        "store_id": user.data["store_id"]
    })

    return {
        "token": token,
        "store_id": user.data["store_id"]
    }
