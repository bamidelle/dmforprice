# DM for Price 🚀

DM for Price is a Social Commerce Operating System that helps merchants turn
"DM for price" messages on WhatsApp and social media into instant orders,
payments, and automated follow-ups.

## Tech Stack
- Streamlit (UI & Dashboard)
- Python (Core logic)
- Supabase (Database)
- FastAPI-style routers (Auth, Products, Orders)

## Project Structure

dmforprice/
├── app.py              # Streamlit entry point
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   └── routers/
│       ├── auth.py
│       ├── products.py
│       └── orders.py
├── requirements.txt
├── .env.example
└── README.md

## How It Runs
- Streamlit Cloud runs `app.py`
- `app.py` imports logic from `backend/`
- Secrets are stored in Streamlit Settings (not in GitHub)

## Deployment
- GitHub Web (code)
- Streamlit Community Cloud (hosting)

## Status
🚧 MVP in active development
