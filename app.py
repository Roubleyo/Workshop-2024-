import streamlit as st
import json
import hashlib
import datetime

# --- FONCTIONS UTILISATEURS ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_user(username, password):
    users = load_users()
    users.append({"username": username, "password": hash_password(password)})
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def check_user(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == hash_password(password):
            return True
    return False

# --- FONCTIONS MESSAGES ---
def load_messages():
    try:
        with open('messages.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_message(username, message):
    messages = load_messages()
    new_message = {
        "id": len(messages) + 1,
        "username": username,
        "message": message,
        "replies": [],
        "timestamp": str(datetime.datetime.now())
    }
    messages.append(new_message)
    with open('messages.json', 'w') as f:
        json.dump(messages, f, indent=4)

def save_reply(message_id, username, reply_message):
    messages = load_messages()
    reply = {
        "id": len(messages) + 1,
        "username": username,
        "message": reply_message,
        "replies": [],
        "timestamp": str(datetime.datetime.now())
    }
    messages.append(reply)
    for message in messages:
        if message["id"] == message_id:
            message["replies"].append(reply["id"])
    with open('messages.json', 'w') as f:
        json.dump(messages, f, indent=4)

# --- PAGE D'INSCRIPTION ---
def show_signup():
    st.title("Inscription")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("S'inscrire"):
        users = load_users()
        if any(user['username'] == username for user in users):
            st.error("Ce nom d'utilisateur existe déjà.")
        else:
            save_user(username, password)
            st.success("Inscription réussie !")

# --- PAGE DE CONNEXION ---
def show_login():
    st.title("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if check_user(username, password):
            st.success("Connexion réussie !")
            st.session_state["username"] = username
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")

# --- PAGE FEED ---
def show_feed():
    if "username" not in st.session_state:
        st.error("Veuillez vous connecter pour accéder au feed.")
        return

    st.title(f"Bienvenue, {st.session_state['username']}!")

    # Publier un message
    st.subheader("Publier un nouveau message")
    new_message = st.text_area("Message")

    if st.button("Publier"):
        if new_message:
            save_message(st.session_state["username"], new_message)
            st.success("Message publié !")
        else:
            st.error("Le message ne peut pas être vide.")

    # Affichage du feed
    st.subheader("Feed des messages")
    messages = load_messages()

    for message in messages:
        st.write(f"{message['username']}: {message['message']} ({message['timestamp']})")

        # Afficher les réponses
        if message["replies"]:
            for reply_id in message["replies"]:
                reply = next((m for m in messages if m["id"] == reply_id), None)
                if reply:
                    st.write(f"  ↳ {reply['username']}: {reply['message']} ({reply['timestamp']})")

        # Répondre à un message
        with st.expander(f"Répondre à {message['username']}"):
            reply_message = st.text_area(f"Réponse au message {message['id']}")
            if st.button(f"Publier la réponse {message['id']}"):
                if reply_message:
                    save_reply(message["id"], st.session_state["username"], reply_message)
                    st.success("Réponse publiée !")
                else:
                    st.error("La réponse ne peut pas être vide.")

# --- LOGIQUE DE NAVIGATION ---
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choisissez une page", ["Connexion", "Inscription", "Feed"])

    if page == "Inscription":
        show_signup()
    elif page == "Connexion":
        show_login()
    elif page == "Feed":
        show_feed()

if __name__ == "__main__":
    main()
