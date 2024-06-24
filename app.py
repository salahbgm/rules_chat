import streamlit as st
from query_data import query_rag

# Interface utilisateur
st.title("Board Game Query App")

# État de la session pour stocker l'historique des chats
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher les messages précédents
for msg in st.session_state.messages:
    if msg["is_user"]:
        st.write(f"Utilisateur: {msg['content']}")
    else:
        st.write(f"Bot: {msg['content']}")

# Saisie de la requête utilisateur
query_text = st.text_input("Entrez votre requête :")

# Bouton Rechercher
if st.button("Rechercher"):
    if query_text:
        # Ajouter le message utilisateur à l'historique des messages
        st.session_state.messages.append({"content": query_text, "is_user": True})

        # Obtenir la réponse du modèle
        response = query_rag(query_text)

        # Ajouter la réponse du modèle à l'historique des messages
        st.session_state.messages.append({"content": response, "is_user": False})

        # Effacer la saisie utilisateur
        st.session_state.input = ""

        # Afficher les messages
        for msg in st.session_state.messages:
            if msg["is_user"]:
                st.write(f"Utilisateur: {msg['content']}")
            else:
                st.write(f"Bot: {msg['content']}")

# Bouton Effacer
if st.button("Effacer"):
    st.session_state.messages = []
    st.experimental_rerun()
