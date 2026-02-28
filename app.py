import streamlit as st

from backend.routers.auth import login_user, signup_user
from backend.routers.orders import create_order, list_orders_for_store, update_order_status
from backend.routers.products import create_product, delete_product, get_products

st.set_page_config(page_title="DM for Price", layout="wide")

for key, default in {
    "authenticated": False,
    "token": None,
    "store_id": None,
    "email": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

if not st.session_state["authenticated"]:
    if st.session_state.get("token") and st.session_state.get("store_id"):
        st.session_state["authenticated"] = True


if not st.session_state["authenticated"]:
    st.title("DM for Price")
    st.caption("Turn social DMs into trackable orders and revenue.")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

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

    with tab2:
        st.subheader("Create an account")
        store_name = st.text_input("Store name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Sign Up"):
            result, store_id = signup_user(email, password, store_name)
            if result == "EMAIL_EXISTS":
                st.error("Email already exists. Please log in.")
                st.stop()
            if result == "STORE_NAME_EMPTY":
                st.error("Store name is required.")
                st.stop()
            if store_id is None:
                st.error("Signup failed")
                st.stop()

            st.session_state["authenticated"] = True
            st.session_state["token"] = result
            st.session_state["store_id"] = store_id
            st.session_state["email"] = email
            st.success("Signup successful! Redirecting...")
            st.rerun()

else:
    st.sidebar.title("DM for Price")
    st.sidebar.caption("Social Commerce OS")
    page = st.sidebar.radio("Navigate", ["Overview", "Products", "Orders", "Settings"])

    st.title("Dashboard")
    st.caption(f"Logged in as {st.session_state['email']}")

    store_id = st.session_state["store_id"]
    products = get_products(store_id)
    orders = list_orders_for_store(store_id)

    if page == "Overview":
        st.subheader("Store Overview")
        total_revenue = sum(float(order.get("total_amount") or 0) for order in orders)
        pending_orders = sum(1 for order in orders if order.get("status") == "pending")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Products", len(products))
        col2.metric("Total Orders", len(orders))
        col3.metric("Pending Orders", pending_orders)
        col4.metric("Revenue", f"₦{total_revenue:,.2f}")

        st.markdown("---")
        st.write("Recent Orders")
        st.dataframe(orders[:10], use_container_width=True)

    elif page == "Products":
        st.subheader("Products")

        with st.form("new_product", clear_on_submit=True):
            name = st.text_input("Product name")
            price = st.number_input("Price", min_value=0.0, step=100.0)
            description = st.text_area("Description")
            submitted = st.form_submit_button("➕ Add New Product")

            if submitted:
                if not name.strip():
                    st.error("Product name is required.")
                else:
                    create_product(store_id, name.strip(), price, description.strip())
                    st.success("Product created.")
                    st.rerun()

        st.markdown("### Product Catalog")
        st.dataframe(products, use_container_width=True)

        if products:
            options = {f"{p['name']} ({p['id']})": p["id"] for p in products}
            target = st.selectbox("Delete a product", list(options.keys()))
            if st.button("Delete Selected Product"):
                delete_product(options[target], store_id)
                st.success("Product deleted.")
                st.rerun()

    elif page == "Orders":
        st.subheader("Orders")

        with st.form("new_order", clear_on_submit=True):
            customer_name = st.text_input("Customer name")
            item_name = st.text_input("Item name")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            total_amount = st.number_input("Total amount", min_value=0.0, step=100.0)
            status = st.selectbox("Status", ["pending", "paid", "fulfilled", "cancelled"])
            submit_order = st.form_submit_button("Create Order")

            if submit_order:
                if not customer_name.strip() or not item_name.strip():
                    st.error("Customer and item name are required.")
                else:
                    create_order(store_id, customer_name.strip(), item_name.strip(), int(quantity), total_amount, status)
                    st.success("Order created.")
                    st.rerun()

        st.markdown("### Order List")
        st.dataframe(orders, use_container_width=True)

        if orders:
            order_options = {
                f"{o.get('customer_name', 'Unknown')} - {o.get('item_name', 'Item')} ({o['id']})": o["id"]
                for o in orders
            }
            selected_order = st.selectbox("Update order", list(order_options.keys()))
            next_status = st.selectbox("New status", ["pending", "paid", "fulfilled", "cancelled"], key="status_update")
            if st.button("Update Status"):
                update_order_status(order_options[selected_order], store_id, next_status)
                st.success("Order updated.")
                st.rerun()

    elif page == "Settings":
        st.subheader("Settings")
        st.write("Store ID:", store_id)
        st.write("Email:", st.session_state["email"])

        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
