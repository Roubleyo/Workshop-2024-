import streamlit as st
import app

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
            app.save_message(st.session_state["username"], new_message)
            st.success("Message publié !")
        else:
            st.error("Le message ne peut pas être vide.")

# Affichage du feed
    st.subheader("Feed des messages")
    messages = app.load_messages()

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
                    app.save_reply(message["id"], st.session_state["username"], reply_message)
                    st.success("Réponse publiée !")
                else:
                    st.error("La réponse ne peut pas être vide.")