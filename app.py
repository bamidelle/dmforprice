import streamlit as st
from backend.routers.auth import login_user, signup_user

st.set_page_config(page_title="DM for Price", layout="wide")

# -------------------------
# Session init
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

    # -------- LOGIN --------
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

    # -------- SIGNUP --------
    with tab2:
        st.subheader("Create an account")

        store_name = st.text_input("Store name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Sign Up"):

            # ✅ new error-safe signup handling
            result, store_id = signup_user(email, password, store_name)

            if result == "EMAIL_EXISTS":
                st.error("Email already exists. Please log in.")
                st.stop()

            if result == "STORE_NAME_EMPTY":
                st.error("Store name is required.")
                st.stop()

            if store_id is None:
                st.error("Signup failed:")
                st.code(result)
                st.stop()

            token = result

            st.session_state["authenticated"] = True
            st.session_state["token"] = token
            st.session_state["store_id"] = store_id
            st.session_state["email"] = email

            st.success("Signup successful! Redirecting...")
            st.rerun()


# =========================
# DASHBOARD
# =========================
else:

    # ---- Sidebar navigation
    st.sidebar.title("DM for Price")
    st.sidebar.caption("Social Commerce OS")

    page = st.sidebar.radio(
        "Navigate",
        ["Overview", "Products", "Orders", "Settings"]
    )

    # ---- Header
    st.title("Dashboard")
    st.caption(f"Logged in as {st.session_state['email']}")

    # ---- Overview
    if page == "Overview":
        st.subheader("Store Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Products", 0)
        col2.metric("Total Orders", 0)
        col3.metric("Revenue", "₦0")

        st.markdown("---")
        st.write("📈 Sales performance and AI insights will appear here.")

    # ---- Products
    elif page == "Products":
        st.subheader("Products")
        st.info("Product management coming next.")
        st.button("➕ Add New Product")

    # ---- Orders
    elif page == "Orders":
        st.subheader("Orders")
        st.info("Orders from Instagram, WhatsApp, and TikTok will appear here.")

    # ---- Settings
    elif page == "Settings":
        st.subheader("Settings")

        st.write("Store ID:", st.session_state["store_id"])
        st.write("Email:", st.session_state["email"])

        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
