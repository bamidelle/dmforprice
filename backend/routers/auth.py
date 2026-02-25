from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from backend.database import supabase
from backend.config import settings

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
def signup_user(email: str, password: str, store_name: str):
    store = supabase.table("stores").insert({
        "name": store_name
    }).execute()

    store_id = store.data[0]["id"]

    user = supabase.table("users").insert({
        "email": email,
        "password": password,
        "store_id": store_id
    }).execute()

    token = create_jwt({
        "user_id": user.data[0]["id"],
        "store_id": store_id
    })

    return token, store_id

@router.post("/login")
def login_user(email: str, password: str):
    response = (
        supabase.table("users")
        .select("*")
        .eq("email", email)
        .eq("password", password)
        .execute()
    )

    if not response.data:
        return None, None

    user = response.data[0]

    token = create_jwt({
        "user_id": user["id"],
        "store_id": user["store_id"]
    })

    return token, user["store_id"]

# -------------------------
# Streamlit-friendly helpers
# -------------------------

def signup_user(email: str, password: str, store_name: str):
    store = supabase.table("stores").insert({
        "name": store_name
    }).execute()

    store_id = store.data[0]["id"]

    user = supabase.table("users").insert({
        "email": email,
        "password": password,
        "store_id": store_id
    }).execute()

    token = create_jwt({
        "user_id": user.data[0]["id"],
        "store_id": store_id
    })

    return token, store_id


def login_user(email: str, password: str):
    response = (
        supabase.table("users")
        .select("*")
        .eq("email", email)
        .eq("password", password)
        .execute()
    )

    if not response.data:
        return None, None

    user = response.data[0]

    token = create_jwt({
        "user_id": user["id"],
        "store_id": user["store_id"]
    })

    return token, user["store_id"]
