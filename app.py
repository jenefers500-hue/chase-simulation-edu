import streamlit as st
import plotly.express as px
from secure_vault import SimulatedChaseEngine
import theme_config as cfg

st.set_page_config(page_title="Chase Personal Simulator", page_icon="🏦", layout="wide")

if 'vault' not in st.session_state:
    st.session_state.vault = SimulatedChaseEngine()

vault = st.session_state.vault
df_acc = vault.get_accounts_summary()
df_ledger = vault.get_transaction_ledger()

st.markdown(
    f"""
    <div style='background-color:{cfg.CHASE_DARK}; padding:18px; border-radius:6px; margin-bottom:20px; border-left: 8px solid {cfg.CHASE_BLUE};'>
        <h1 style='color:white; margin:0; font-family:sans-serif; font-size:26px;'>CHASE 🏦</h1>
        <p style='color:#b0c4de; margin:4px 0 0 0; font-size:13px;'>Secure Simulation Environment • Historical Verification Ledger</p>
    </div>
    """, 
    unsafe_allow_html=True
)

st.subheader("Your Financial Accounts Overview")
cols = st.columns(len(df_acc))
for idx, row in df_acc.iterrows():
    with cols[idx]:
        st.metric(label=row['account_name'], value=f"${row['balance']:,.2f}")

st.markdown("---")
left_panel, right_panel = st.columns([1, 1.2])

with left_panel:
    st.markdown(f"<h3 style='color:{cfg.CHASE_DARK};'>📥 Post Transaction Entry</h3>", unsafe_allow_html=True)

    selected_name = st.selectbox("Choose Targeted Simulation Account:", df_acc['account_name'].tolist())
    target_id = df_acc[df_acc['account_name'] == selected_name].iloc[0]['account_id']

    tx_type = st.radio("Accounting Ledger Allocation:", ["Expense", "Income"], horizontal=True)
    categories = ["Cash", "Transfer", "Groceries", "Utilities", "Dining Out", "Uncategorized"]
    category = st.selectbox("Budget Categorization Tag:", categories)

    description = st.text_input("Transaction Description / Memo:", placeholder="e.g. ATM Withdrawal - Owner Verified")
    amount = st.number_input("Transaction Volume Currency Amount ($):", min_value=0.01, step=0.01, format="%.2f")

    if st.button("Authorize & Post Transaction to Sandbox", type="primary"):
        vault.record_transaction(target_id, description, category, amount, tx_type)
        st.success("Transaction verified, logged to ledger database, and balances recalculated.")
        st.rerun()

with right_panel:
    st.markdown(f"<h3 style='color:{cfg.CHASE_DARK};'>📊 Simulation Category Metrics</h3>", unsafe_allow_html=True)

    expenses_only = df_ledger[(df_ledger['amount'] < 0) & (df_ledger['status'] == 'Completed')].copy()
    expenses_only['abs_amount'] = expenses_only['amount'].abs()

    if not expenses_only.empty:
        fig = px.pie(
            expenses_only, 
            values='abs_amount', 
            names='category', 
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Darkmint
        )
        fig.update_layout(margin=dict(t=20, b=10, l=10, r=10), height=280)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No completed debit histories available to compile chart models.")

st.markdown("---")
st.markdown(f"<h3 style='color:{cfg.CHASE_DARK};'>📜 Historical Transaction Ledger Statement</h3>", unsafe_allow_html=True)

st.dataframe(
    df_ledger,
    column_config={
        "transaction_id": "Transaction ID",
        "date": "Posting Time (ISO)",
        "account_name": "Account Link",
        "description": "Description",
        "category": "Category",
        "amount": st.column_config.NumberColumn("Amount ($)", format="$%.2f"),
        "status": "Status Flag",
        "running_balance": st.column_config.NumberColumn("Running Balance ($)", format="$%.2f")
    },
    use_container_width=True,
    hide_index=True
)
