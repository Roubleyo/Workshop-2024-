import streamlit as st
import app
import datetime
from app import save_user

# --- PAGE DE CONNEXION ---
def show_login():
    if 'inscription' not in st.session_state:
        st.session_state['inscription'] = False
        st.session_state['mineur'] = False

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
                    return True
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect")
                    return False
        with d : 
            if st.button("Pas de compte ?"):
                st.session_state['inscription'] = True
                st.rerun()
        
    if st.session_state['inscription'] == True : 
        with placeholder.container() : 
            birth = st.date_input("Age",min_value=datetime.date(1900,1,1),)
            age = datetime.date.today().year-birth.year
            if age < 13 :
                st.text("L'age minimum pour créer un compte est de 13 ans.")
            elif age >= 13 and age < 18:
                tel = st.text_input("Numéro de téléphone du représentant légal")
            else :
                tel = st.text_input("Numéro de téléphone")
        with g : 
            if st.button("Inscription"):
                age = datetime.date.today().year-birth.year
                users = app.load_users()
                if any(user['username'] == username for user in users):
                    st.error("Ce nom d'utilisateur existe déjà.")
                elif age < 13:
                    st.error("L'age minimum pour créer un compte est de 13 ans !")
                else:
                    user= {"username": username, "password": password, "age": age, "tel": tel}
                    save_user(user)
                    st.session_state['inscription'] = False
                    st.rerun()
        with d : 
            if st.button("Déjà un compte ?"):
                    st.session_state['inscription'] = False
                    st.rerun()
    