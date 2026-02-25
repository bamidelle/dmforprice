import streamlit as st

class Settings:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    JWT_SECRET = st.secrets.get("JWT_SECRET", "dev-secret")



