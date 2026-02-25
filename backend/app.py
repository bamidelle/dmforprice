import streamlit as st
from backend.routers.auth import login_user, signup_user

st.set_page_config(page_title="DM for Price")

# -------------------------
# Session state
# -------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "store_id" not in st.session_state:
    st.session_state.store_id = None

# -------------------------
# Login / Signup UI
# -------------------------
st.title("DM for Price")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

with tab1:
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        token, store_id = login_user(email, password)

        if token:
            st.session_state.token = token
            st.session_state.store_id = store_id
            st.success("Logged in successfully 🎉")
            st.rerun()
        else:
            st.error("Invalid email or password")

with tab2:
    st.subheader("Create an account")

    store_name = st.text_input("Store name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        token, store_id = signup_user(email, password, store_name)

        st.session_state.token = token
        st.session_state.store_id = store_id
        st.success("Account created 🎉")
        st.rerun()
