from fastapi import APIRouter
from datetime import datetime, timedelta
import jwt
import bcrypt

from backend.database import supabase
from backend.config import JWT_SECRET

router = APIRouter()

# -------------------------
# JWT Helper
# -------------------------
def create_jwt(payload: dict):
    payload["exp"] = datetime.utcnow() + timedelta(days=7)
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


# =========================
# SIGNUP
# =========================
def signup_user(email: str, password: str, store_name: str):

    # 1️⃣ Check if user already exists
    existing = (
        supabase.table("users")
        .select("id")
        .eq("email", email)
        .execute()
    )

    if existing.data:
        return None, None  # email already exists

    # 2️⃣ Create store
    store = supabase.table("stores").insert({
        "name": store_name
    }).execute()

    store_id = store.data[0]["id"]

    # 3️⃣ Hash password
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # 4️⃣ Create user
    user = supabase.table("users").insert({
        "email": email,
        "password_hash": password_hash,
        "store_id": store_id
    }).execute()

    # 5️⃣ Generate token
    token = create_jwt({
        "user_id": user.data[0]["id"],
        "store_id": store_id
    })

    return token, store_id


# =========================
# LOGIN
# =========================
def login_user(email: str, password: str):

    response = (
        supabase.table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not response.data:
        return None, None

    user = response.data[0]

    # 🔐 Verify password
    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    ):
        return None, None

    token = create_jwt({
        "user_id": user["id"],
        "store_id": user["store_id"]
    })

    return token, user["store_id"]
