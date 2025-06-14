import base64
import requests
import os
from mistralai import Mistral
from dotenv import load_dotenv


load_dotenv()

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None

# Path to your image
image_path = "C:/Users/horai/Documents/projets/jpo/image.png"

# Getting the base64 string
base64_image = encode_image(image_path)

# Retrieve the API key from environment variables
api_key = os.environ["MISTRAL_API_KEY"]

# Specify model
model = "pixtral-large-latest"

# Initialize the Mistral client
client = Mistral(api_key=api_key)

# Define the messages for the chat
messages = [
    {
        "role": "system",
        "content" : "Tu es un assistant capillaire un peu espiègle qui analyse la photo d’un utilisateur (visage) et lui recommande une coupe de cheveux flatteuse — mais toujours avec une petite pique gentille ou une touche d’humour. L’objectif est de divertir l’utilisateur tout en lui proposant une vraie idée de coupe adaptée à sa morphologie et à son style perçu."    
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Tu es un(e) expert(e) en coiffure doté(e) d’un humour bien aiguisé. À partir de la photo du visage de l’utilisateur, donne une recommandation de coupe de cheveux tendance et flatteuse. Mais attention : sois toujours un peu taquin(e), comme un(e) ami(e) qui n’a pas sa langue dans sa poche."
            },
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}" 
            }
        ]
    }
]

# Get the chat response
chat_response = client.chat.complete(
    model=model,
    messages=messages
)

# Print the content of the response
print(chat_response.choices[0].message.content)