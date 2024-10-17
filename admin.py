import streamlit as st
import app
import pandas as pd
import json
from bert_toxicity import check_text


# --- PAGE FEED ---
def show_admin():
    if st.session_state['admin'] == False:
        st.error("Veuillez vous connecter en tant qu'admin.")
        return

    st.title(f"Bienvenue dans le mode administration, {st.session_state['username']}!")

    # Publier un message
    # st.subheader("Publier un nouveau message")
    user_json = app.load_users()
    users = pd.DataFrame(user_json)
    users['select'] = [False] * len(users)

    users = users.sort_values(by='strike', ascending=False)

    a = st.data_editor(users,
                   column_order=['select','username','strike','age','admin'],
                   column_config= {
                            "username" : "Username",
                            "password" :  "Password",
                            "age"      : "Age",
                            "parentnum": "Contact",
                            "strike"   : "Strikes",
                            "admin"    : "Admin ?",
                            "select" : "Select ? "
                                   },
                                   use_container_width= True,
                                   hide_index= True)
    

    b = a[a['select'] == True] 

    #st.write(b)
    #st.write('IIII')

    msg_json = app.load_messages()
    msgs = pd.DataFrame(msg_json)
    for index, row in b.iterrows():
        #st.write(f"Row {index}:")
        st.info(f"""Username: {row['username']},
                 Age: {row['age']},
                 Admin: {row['admin']}""")



        a = st.dataframe(
                     msgs[msgs['username'] == row['username']],
                     column_order=['message','replies','toxicity','timestamp'],
                     use_container_width=True,
                     hide_index = True,
                     on_select="rerun",
                     selection_mode="single-row")
        

        

        erase = st.button('Erase')
        msg_chosi = msgs.iloc[a.selection.rows]
        #st.dataframe(msg_chosi,use_container_width=True,)
        if not msg_chosi.empty and erase : 
            id = msg_chosi.iloc[0]['id']
            username = msg_chosi.iloc[0]['username']



            msg_json = app.load_messages()
     
            filtered_data = [msg for msg in msg_json if msg['id'] != id]


            for msg in filtered_data:
                msg['replies'] = [reply_id for reply_id in msg['replies'] if reply_id != id]

            #st.write(filtered_data)

            with open('messages.json', 'w') as f:
                json.dump(filtered_data, f, indent=4)

            
            for user in user_json:
                if user["username"] == username :
                    user["strike"] += 1

            with open('users.json', 'w') as f:
                json.dump(user_json, f, indent=4)

            #st.write(user_json)


            st.success('Message bien supprimé !')


          





        


#efface msgs  + ajoute strike 


    
    



