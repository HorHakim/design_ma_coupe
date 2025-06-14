import streamlit as st
import base64
import requests
import os
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

# Streamlit app
st.set_page_config(page_title="HairCut GPT 💇‍♂️", page_icon="💇‍♀️", layout="centered")
st.title("💇‍♀️ Quelle coupe te va vraiment ?")
st.markdown("**Uploade ta photo et découvre ce que ton futur toi capillaire pourrait être... avec une petite touche de sarcasme ! 😏**")

# Image uploader
uploaded_file = st.file_uploader("📸 Choisis une photo de ton visage", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Affiche l’image uploadée
    st.image(uploaded_file, caption="C’est toi ça ? On va voir ce qu’on peut faire... 😎", use_container_width =True)

    # Encode image
    base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')

    # Initialize the Mistral client
    client = Mistral(api_key=api_key)

    # Messages à envoyer à Pixtral
    messages = [
        {
            "role": "system",
            "content": (
                "Tu es un assistant capillaire un peu espiègle qui analyse la photo d’un utilisateur "
                "et lui recommande une coupe de cheveux flatteuse — avec une petite pique gentille ou une touche d’humour. "
                "L’objectif est de divertir l’utilisateur tout en lui proposant une vraie idée de coupe adaptée à sa morphologie et à son style perçu."
            )
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Tu es un(e) expert(e) en coiffure doté(e) d’un humour bien aiguisé. "
                        "À partir de la photo du visage de l’utilisateur, donne une recommandation de coupe de cheveux tendance et flatteuse. "
                        "Mais attention : sois toujours un peu taquin(e), comme un(e) ami(e) qui n’a pas sa langue dans sa poche."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ]

    # Appel API avec spinner
    with st.spinner("Analyse en cours... 😬"):
        try:
            chat_response = client.chat.complete(
                model="pixtral-large-latest",
                messages=messages
            )
            st.success("Voilà le verdict ! 💇‍♂️")
            st.markdown(chat_response.choices[0].message.content)

        except Exception as e:
            st.error("Erreur lors de l'appel à l'API. Vérifie ta clé API et ta connexion.")
            st.exception(e)
