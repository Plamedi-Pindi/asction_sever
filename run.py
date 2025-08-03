# run.py
import actions  # Isso garante que todas as actions sejam carregadas
from rasa_sdk import endpoint

if __name__ == "__main__":
    endpoint.run("actions")
