import streamlit as st
import requests
import plotly.express as px

# ─── PAGE CONFIG ────────────────────────────────
st.set_page_config(
    page_title="CoinStack Dashboard",
    page_icon="💱",
    layout="wide"
)

# ─── CUSTOM CSS ─────────────────────────────────
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background-color: #f4f6f9;
    font-family: 'Segoe UI', sans-serif;
}

/* Main Layout */
.dashboard {
    display: flex;
    height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 250px;
    background-color: #111827;
    color: white;
    padding: 30px 20px;
}

.sidebar h2 {
    color: white;
    margin-bottom: 40px;
}

.sidebar p {
    color: #9ca3af;
    margin: 18px 0;
    cursor: pointer;
    font-size: 15px;
}

.sidebar p:hover {
    color: white;
}

/* Main Content */
.main-content {
    flex: 1;
    padding: 40px;
    overflow-y: auto;
}

/* Card */
.card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* Result Box */
.result-box {
    background: #16a34a;
    color: white;
    padding: 20px;
    border-radius: 12px;
    font-size: 22px;
    font-weight: 600;
    text-align: center;
    margin-top: 20px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #16a34a);
    color: white !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.2rem !important;
    font-size: 16px !important;
    border: none !important;
    font-weight: 600;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #16a34a, #2563eb);
}
</style>
""", unsafe_allow_html=True)

# ─── START DASHBOARD STRUCTURE ──────────────────
st.markdown("""
<div class="dashboard">

    <div class="sidebar">
        <h2>💱 CoinStack</h2>
        <p>Dashboard</p>
        <p>Converter</p>
        <p>Analytics</p>
        <p>Settings</p>
    </div>

    <div class="main-content">
""", unsafe_allow_html=True)

st.title("💱 Real-Time Currency Converter")

# 🌍 Currency list
CURRENCIES = [
    "USD", "INR", "EUR", "GBP", "JPY", "AUD", "CAD",
    "CHF", "CNY", "SGD", "NZD", "ZAR"
]

# ─── INPUT SECTION ──────────────────────────────
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🔁 Convert Currency")

amount = st.number_input("Amount", min_value=0.01, value=1000.0)

col1, col2 = st.columns(2)
with col1:
    from_currency = st.selectbox("From", CURRENCIES, index=0)
with col2:
    to_currency = st.selectbox("To", CURRENCIES, index=1)

st.markdown("</div>", unsafe_allow_html=True)

# ─── FEES SECTION ──────────────────────────────
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("💸 Taxes & Fees")

exchange_margin = st.slider("Exchange Margin (%)", 0.0, 10.0, 2.5)
transaction_fee = st.slider("Transaction Fee (%)", 0.0, 5.0, 1.0)
fixed_fee = st.number_input("Fixed Service Fee", value=5.0)

st.markdown("</div>", unsafe_allow_html=True)

# ─── ACTION ─────────────────────────────────────
if st.button("🚀 Convert", use_container_width=True):
    with st.spinner("Fetching live exchange rate..."):
        response = requests.get(
            "http://127.0.0.1:8000/convert",
            params={
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "exchange_margin": exchange_margin,
                "fixed_fee": fixed_fee,
                "transaction_fee": transaction_fee,
            }
        )

    if response.status_code == 200:
        data = response.json()

        # Result Box
        st.markdown(
            f"<div class='result-box'>🔥 Final Amount: {data['final_amount']} {to_currency}</div>",
            unsafe_allow_html=True
        )

        # ─── FEE BREAKDOWN ──────────────────────────
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Fee Breakdown")

        fee_data = {
            "Component": [
                "Converted Amount",
                "Exchange Margin",
                "Transaction Fee",
                "Fixed Fee"
            ],
            "Amount": [
                data["converted_amount"],
                data["exchange_margin_cost"],
                data["transaction_fee_cost"],
                data["fixed_fee"],
            ]
        }

        fig = px.bar(
            fee_data,
            x="Component",
            y="Amount",
            text_auto=True,
            color="Component",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Raw JSON
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        with st.expander("🔍 View Raw API Response"):
            st.json(data)
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("❌ Backend error")
        st.text(response.text)

# ─── CLOSE DASHBOARD STRUCTURE ──────────────────
st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)