import streamlit as st
import pandas as pd
import os
import hashlib

# Set up Streamlit page
st.set_page_config(page_title="Blood Bank Finder", page_icon="💉", layout="centered")

# Load custom CSS for styling
try:
    with open("css/style.css", "r") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Custom styles are missing. Default styles will be used.")

# Helper Functions
def hash_password(password):
    """Hashes a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_user_data():
    """Loads user data from CSV."""
    if os.path.exists("user_data/users.csv"):
        return pd.read_csv("user_data/users.csv")
    else:
        return pd.DataFrame(columns=["Name", "Age", "Blood Group", "Username", "Password"])

def save_user_data(data):
    """Saves user data to CSV."""
    os.makedirs("user_data", exist_ok=True)
    data.to_csv("user_data/users.csv", index=False)

# Initialize user data
user_data = load_user_data()

# Tabs for Navigation
tabs = st.tabs(["Create Account", "Login"])

with tabs[0]:
    st.header("🔐 Create Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    username = st.text_input("Choose a Username")
    password = st.text_input("Create a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not (name and username and password and confirm_password):
            st.error("All fields are required!")
        elif password != confirm_password:
            st.error("Passwords do not match!")
        elif username in user_data["Username"].values:
            st.error("Username already exists. Choose another one!")
        else:
            # Save user data
            hashed_pw = hash_password(password)
            new_user = pd.DataFrame(
                [[name, age, blood_group, username, hashed_pw]],
                columns=["Name", "Age", "Blood Group", "Username", "Password"],
            )
            user_data = pd.concat([user_data, new_user], ignore_index=True)
            save_user_data(user_data)
            st.success("Account created successfully! You can now log in.")

with tabs[1]:
    st.header("🔓 Login")
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed_pw = hash_password(login_password)
        user = user_data[
            (user_data["Username"] == login_username)
            & (user_data["Password"] == hashed_pw)
        ]
        if not user.empty:
            st.success(f"Welcome back, {user.iloc[0]['Name']}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = login_username
        else:
            st.error("Invalid username or password.")

if st.session_state.get("logged_in", False):
    with tabs[2]:
        st.header("💉 Find Blood Banks")
        # Dummy blood bank data
        blood_banks = [
            {"name": "City Blood Bank", "location": "Saddar", "contact": "0301-1234567", "blood_groups": ["A+", "B+"]},
            {"name": "LifeSaver Blood Center", "location": "Gulshan", "contact": "0302-2345678", "blood_groups": ["O+", "AB+"]},
        ]

        selected_blood_group = st.selectbox("Select Blood Group", ["A+", "B+", "O+", "AB+"])
        for bank in blood_banks:
            if selected_blood_group in bank["blood_groups"]:
                st.markdown(
                    f"""
                    <div class="blood-bank" style="border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 5px;">
                        <h4 style="color: #E63946;">{bank['name']}</h4>
                        <p><strong>Location:</strong> {bank['location']}</p>
                        <p><strong>Contact:</strong> {bank['contact']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
