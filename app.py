import streamlit as st
from backend.routers.auth import login_user, signup_user

st.set_page_config(page_title="DM for Price")

# -------------------------
# Session state (init)
# -------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "token" not in st.session_state:
    st.session_state["token"] = None

if "store_id" not in st.session_state:
    st.session_state["store_id"] = None

if "email" not in st.session_state:
    st.session_state["email"] = None

# -------------------------
# Restore session on refresh
# -------------------------
if not st.session_state["authenticated"]:
    if st.session_state.get("token") and st.session_state.get("store_id"):
        st.session_state["authenticated"] = True


# =========================
# AUTH SCREENS
# =========================
if not st.session_state["authenticated"]:

    st.title("DM for Price")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # ---------------- LOGIN ----------------
    with tab1:
        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            token, store_id = login_user(email, password)

            if token:
                st.session_state["authenticated"] = True
                st.session_state["token"] = token
                st.session_state["store_id"] = store_id
                st.session_state["email"] = email

                st.success("Logged in successfully 🎉")
                st.rerun()
            else:
                st.error("Invalid email or password")

    # ---------------- SIGNUP ----------------
    with tab2:
        st.subheader("Create an account")

        store_name = st.text_input("Store name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Sign Up"):
            token, store_id = signup_user(email, password, store_name)

            if token:
                st.session_state["authenticated"] = True
                st.session_state["token"] = token
                st.session_state["store_id"] = store_id
                st.session_state["email"] = email

                st.success("Signup successful! Redirecting...")
                st.rerun()
            else:
                st.error("Signup failed")


# =========================
# DASHBOARD (TEMP)
# =========================
else:
    st.title("DM for Price Dashboard")

    st.write("Welcome 👋")
    st.write("Store ID:", st.session_state["store_id"])
    st.write("Email:", st.session_state["email"])

    # Proper logout wipe
    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
