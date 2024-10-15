import streamlit as st
import json
import hashlib
import datetime
import login
import feed

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
    print(user)
    users = load_users()
    users.append({"username": user['username'], "password": hash_password(user['password']), "age": user["age"], "parentnum":user["tel"]})
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
        "type": 'message',
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
        "type": 'reply',
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
    page = st.sidebar.selectbox("Choisissez une page", ["Connexion", "Feed"])

    if page == "Connexion":
        login.show_login()
    elif page == "Feed":
        feed.show_feed()

if __name__ == "__main__":
    main()
