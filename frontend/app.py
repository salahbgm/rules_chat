import streamlit as st
from scripts.query_data import query_rag


def select_board_game():
    board_games = [
        "Monopoly",
        "La Bonne Paye"
    ]
    return st.selectbox("Sélectionner un jeu de société :", board_games)


def display_messages(messages):
    for msg in messages:
        st.write("---")
        if msg["is_user"]:
            st.write(f"Utilisateur: {msg['content'][39:]}")
        else:
            st.markdown(f"### Bot: {msg['content']['response'].content}")
            st.write(f"Sources : {msg['content']['sources']}")


def handle_query(query_text, messages):
    if query_text:
        # Ajouter le message utilisateur à l'historique des messages
        messages.append({"content": query_text, "is_user": True})

        # Obtenir la réponse du modèle
        response = query_rag(query_text)

        # Ajouter la réponse du modèle à l'historique des messages
        messages.append({"content": response, "is_user": False})


def init():
    # État de la session pour stocker l'historique des chats
    if "messages" not in st.session_state:
        st.session_state.messages = []


def main():
    st.title("Board Game Query App")

    # Initial setup
    init()

    # Afficher les messages précédents
    display_messages(st.session_state.messages)

    # Sélection du jeu de société
    board_game = select_board_game()

    # Saisie de la requête utilisateur
    query_text = st.text_input("Entrez votre requête :")

    # Ajouter le nom du jeu de société à la requête
    full_query_text = f"Le jeu de société est {board_game}:\n\n {query_text}"

    # Bouton Rechercher
    if st.button("Rechercher"):
        handle_query(full_query_text, st.session_state.messages)
        display_messages(st.session_state.messages)

    # Bouton Effacer
    if st.button("Effacer"):
        st.session_state.messages = []
        st.rerun()


if __name__ == '__main__':
    main()
