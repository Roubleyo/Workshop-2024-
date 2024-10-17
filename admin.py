import streamlit as st
import app
from bert_toxicity import check_text


# --- PAGE FEED ---
def show_admin():
    if st.session_state['admin'] == False:
        st.error("Veuillez vous connecter en tant qu'admin.")
        return

    st.title(f"Bienvenue dans le mode administration, {st.session_state['username']}!")

    # Publier un message
    # st.subheader("Publier un nouveau message")
    new_message = st.chat_input("Publier un nouveau message!")

    # if st.button("Publier"):
    if new_message:
        toxicity = check_text(new_message)
        if toxicity['toxicity'] > 0.80:
            st.error("Le message est inapproprié, vous ne pouvez pas dire cela sur notre réseau")
        else:
            app.save_message(st.session_state["username"], new_message)
            st.rerun()
        # st.success("Message publié !")
    # else:
    # st.error("Le message ne peut pas être vide.")

    # Affichage du feed
    st.subheader("Feed des messages")
    messages = app.load_messages()
    i = 0
    for message in messages:
        i += 1
        if message['type'] == 'message':
            # st.write(f"{message['username']}: {message['message']} ({message['timestamp']})")
            msg_box = st.chat_message(message['username'])  # ,message['message'])
            msg_box.write(f"""**{message['timestamp'][:19]}** """)
            with st.expander(f"""**{message['username']}** :  {message['message']}"""):
                if message["replies"]:
                    for reply_id in message["replies"]:
                        reply = next((m for m in messages if m["id"] == reply_id), None)
                        if reply:
                            st.write(f"({reply['timestamp'][:19]}) **↳** {reply['username']}: {reply['message']} ")
                # else :
                # msg_box.write(message['message'])

                # Répondre à un message
                # with st.expander(f"Répondre à {message['username']}"):
                reply_message = st.text_area(f"Réponse au message", key=i)
                if st.button(f"Publier la réponse {message['id']}"):
                    if reply_message:
                        toxicity = check_text(reply_message)
                        if toxicity['toxicity'][0] > 0.80:
                            st.error("Le message est inapproprié, vous ne pouvez pas dire cela sur notre réseau")
                        else:
                            app.save_reply(message["id"], st.session_state["username"], reply_message,
                                           toxicity['toxicity'][0])
                            st.success("Réponse publiée !")
                            st.rerun()
                    else:
                        st.error("La réponse ne peut pas être vide.")
