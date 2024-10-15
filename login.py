import streamlit as st
import app

# --- PAGE DE CONNEXION ---
def show_login():
    if 'inscription' not in st.session_state:
        st.session_state['inscription'] = False

    if st.session_state['inscription'] != True:
        st.title("Connexion")
    else:
        st.title("Inscription")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    placeholder = st.empty()
    g,d = st.columns([3.75,1])
    if st.session_state['inscription'] != True :
        with g : 
            if st.button("Se connecter"):
                if app.check_user(username, password):
                    st.success("Connexion réussie !")
                    st.session_state["username"] = username
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect")
        with d : 
            if st.button("Pas de compte ?"):
                st.session_state['inscription'] = True
                st.rerun()
        
    if st.session_state['inscription'] == True : 
        with placeholder.container() : 
            age = st.text_input("Age")
        with g : 
            if st.button("Inscription"):
                users = app.load_users()
                if any(user['username'] == username for user in users):
                    st.error("Ce nom d'utilisateur existe déjà.")
                else:
                    app.save_user(username, password, age)
                    st.success("Inscription réussie !")
        with d : 
            if st.button("Déjà un compte ?"):
                    st.session_state['inscription'] = False
                    st.rerun()
    