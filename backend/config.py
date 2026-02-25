import streamlit as st

class Settings:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

settings = Settings()
JWT_SECRET = st.secrets.get("JWT_SECRET", "dev-secret")
