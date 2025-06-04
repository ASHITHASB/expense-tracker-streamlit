
import streamlit as st
import pandas as pd
import os

EXPENSES_FILE = "expenses.csv"
BUDGET_FILE = "budget.txt"

# Initialize or load data
def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        return pd.read_csv(EXPENSES_FILE)
    return pd.DataFrame(columns=["date", "category", "amount", "description"])

def save_expenses(df):
    df.to_csv(EXPENSES_FILE, index=False)

def load_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as f:
            try:
                return float(f.read().strip())
            except:
                return 0.0
    return 0.0

def save_budget(budget):
    with open(BUDGET_FILE, "w") as f:
        f.write(str(budget))

# App layout
st.title("💰 Personal Expense Tracker")

# Load data
df = load_expenses()
budget = load_budget()

# Sidebar: Add Expense
st.sidebar.header("➕ Add New Expense")
with st.sidebar.form("expense_form"):
    date = st.date_input("Date")
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        new_exp = pd.DataFrame([{
            "date": date,
            "category": category,
            "amount": amount,
            "description": description
        }])
        df = pd.concat([df, new_exp], ignore_index=True)
        save_expenses(df)
        st.success("Expense added!")

# Sidebar: Set Budget
st.sidebar.header("💵 Set Monthly Budget")
new_budget = st.sidebar.number_input("Monthly Budget", min_value=0.0, value=budget, format="%.2f")
if st.sidebar.button("Save Budget"):
    save_budget(new_budget)
    st.sidebar.success(f"Budget set to ${new_budget:.2f}")

# Main: View and Track
st.subheader("📋 All Expenses")
if df.empty:
    st.info("No expenses recorded.")
else:
    st.dataframe(df)

# Budget tracking
total_spent = df["amount"].sum()
st.subheader("📊 Budget Summary")
st.markdown(f"**Monthly Budget:** ₹ {budget:.2f}")
st.markdown(f"**Total Spent:** ₹ {total_spent:.2f}")
if budget > 0:
    if total_spent > budget:
        st.error("🚨 You have exceeded your budget!")
    else:
        st.success(f"✅ You have ₹ {budget - total_spent:.2f} remaining.")
