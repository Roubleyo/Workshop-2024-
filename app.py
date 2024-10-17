import streamlit as st
import json
import hashlib
import datetime
import login
import feed
import admin


# --- FONCTIONS UTILISATEURS ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_user(user):
    users = load_users()
    users.append({"username": user['username'], "password": hash_password(user['password']), "age": user["age"], "parentnum":user["tel"], "strike":0, "admin": False})
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


def save_message(username, message, toxicity):
    messages = load_messages()
    new_message = {
        "id": len(messages) + 1,
        "username": username,
        "message": message,
        "replies": [],
        "type": 'message',
        "toxicity": toxicity,
        "timestamp": str(datetime.datetime.now())
    }
    messages.append(new_message)
    with open('messages.json', 'w') as f:
        json.dump(messages, f, indent=4)


def save_reply(message_id, username, reply_message, toxicity):
    messages = load_messages()
    reply = {
        "id": len(messages) + 1,
        "username": username,
        "message": reply_message,
        "replies": [],
        "type": 'reply',
        "toxicity": toxicity,
        "timestamp": str(datetime.datetime.now())
    }
    messages.append(reply)
    for message in messages:
        if message["id"] == message_id:
            message["replies"].append(reply["id"])
    with open('messages.json', 'w') as f:
        json.dump(messages, f, indent=4)


# --- LOGIQUE DE NAVIGATION ---
def main():
    st.sidebar.title("Navigation")
    if 'lst' not in st.session_state:
        st.session_state['lst'] = ["Connexion", "Feed","Administration"]


    page = st.sidebar.selectbox("Choisissez une page", st.session_state['lst'])

    if 'page' not in st.session_state:
        st.session_state['page'] = "Connexion"
    else:
        st.session_state['page'] = page

    if st.session_state['page'] == "Connexion":
        test = login.show_login()
        if test ==  True:
            st.session_state['page'] = "Feed"
            st.session_state['lst'] = ["Feed", "Connexion","Administration"]
            st.rerun()
    elif st.session_state['page'] == "Feed":
        feed.show_feed()
    elif st.session_state['page'] == "Administration":
        admin.show_admin()


if __name__ == "__main__":
    main()
