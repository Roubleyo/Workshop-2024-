import streamlit as st
import app

# --- PAGE DE CONNEXION ---
def show_login():
    st.title("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if app.check_user(username, password):
            st.success("Connexion réussie !")
            st.session_state["username"] = username
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")