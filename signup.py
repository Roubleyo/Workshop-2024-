import streamlit as st
import app

# --- PAGE D'INSCRIPTION ---
def show_signup():
    st.title("Inscription")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("S'inscrire"):
        users = app.load_users()
        if any(user['username'] == username for user in users):
            st.error("Ce nom d'utilisateur existe déjà.")
        else:
            app.save_user(username, password)
            st.success("Inscription réussie !")