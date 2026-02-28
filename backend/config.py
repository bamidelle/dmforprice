import os
import streamlit as st


def _get_secret(name: str, default: str | None = None) -> str:
    """Read from Streamlit secrets first, then environment variables."""
    try:
        value = st.secrets.get(name)
    except Exception:
        value = None

    if value is None:
        value = os.getenv(name, default)

    if value is None:
        raise RuntimeError(f"Missing required config value: {name}")

    return value


SUPABASE_URL = _get_secret("SUPABASE_URL", "")
SUPABASE_KEY = _get_secret("SUPABASE_KEY", "")
JWT_SECRET = _get_secret("JWT_SECRET", "dev-secret")
