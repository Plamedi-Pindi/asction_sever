from typing import Any, Text, Dict, List

from openai import OpenAI
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

Alunos = [
    {"numeroEst": "12345", "senha": "abc123"},
    {"numeroEst": "67890", "senha": "senha456"},
]  

# print("✅ O arquivo actions.py foi carregado com sucesso.")

from rasa_sdk.interfaces import Action


########## #############
class ActionFindCourse(Action):
    def name(self) -> Text:
        return "action_consultar_curso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        API = os.getenv("API_ENDPOINT")  
        
        if not API:
            dispatcher.utter_message(text="⚠️ O sistema está fora do ar no momento. Tente mais tarde.")
            return []
        
        curso_especifico  = tracker.get_slot("curso_especifico_slt")

        response = requests.get(f"{API}/cursosinfo?termo={curso_especifico}")
        if response.status_code == 200:
            message = response.json()
            if message["isList"] == False:
                dispatcher.utter_message(text=message["details"])
                return [SlotSet("curso_especifico_slt", None)]
                
            if message["isList"] == True:
                response =  (
                    "### 📘 A **UMA** possui muitos cursos de **engenharia**\n"
                    "Qual especificamente gostarias de saber?\n" +
                    "\n".join(f"- {curso}" for curso in message['cursos'])
                )
                dispatcher.utter_message(text=response)
                return [SlotSet("curso_especifico_slt", None)]
            
            if "isFound" in message and message["isFound"] == False:
                response = (
                    f"⚠️ O curso **{curso_especifico}** não foi encontrado na base de dados da UMA.\n\n"
                    "Poderias verificar se escreveste corretamente ou tentar outro curso?"
                )
                dispatcher.utter_message(text= response)
                return [SlotSet("curso_especifico_slt", None)]
            
        else:
            try:
                message = response.json()
                dispatcher.utter_message(text=message.get("message", "Erro ao consultar o curso."))
            except:
                dispatcher.utter_message(text="❌ Ocorreu um erro ao consultar o curso. Tente novamente mais tarde.")
        return []


class ActionValidarCredenciais(Action):

    def name(self) -> Text:
        return "action_validar_credenciais"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Pegar os dados do aluno
        numeroEstudante = tracker.get_slot("numero_estudante_slt")
        senhaEstudante = tracker.get_slot("senha_estudante_slt")
        tentativas = tracker.get_slot("tentativas_login") or 0


        autenticado = False

        for aluno in Alunos:
            if aluno["numeroEst"] == numeroEstudante and aluno["senha"] == senhaEstudante:
                autenticado = True
                break

        if autenticado:
            dispatcher.utter_message(text="✅ Autenticação bem-sucedida.")
            return [
                SlotSet("is_authenticated", True),
                SlotSet("tentativas_login", 0)
            ]
        else:
            tentativas += 1
            if tentativas >= 3:
                dispatcher.utter_message(text="❌ Número de tentativas excedido. Por favor, procure o atendimento humano.")
                return [
                    SlotSet("is_authenticated", False),
                    SlotSet("numero_estudante_slt", None),
                    SlotSet("senha_estudante_slt", None),
                    SlotSet("tentativas_login", 0)
                ]
            else:
                dispatcher.utter_message(
                    text=f"❌ Número de estudante ou senha incorretos. Tentativa {int(tentativas)}/3. Tente novamente.")
                return [
                    SlotSet("is_authenticated", False),
                    SlotSet("numero_estudante_slt", None),
                    SlotSet("senha_estudante_slt", None),
                    SlotSet("tentativas_login", tentativas)
                ]
                

class ActionAskOpenAI(Action):
    def name(self):
        return "action_ask_openai"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict):
        
         # API Key da OpenAI (coloque em variável de ambiente para segurança)
        # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        client = OpenAI(api_key=os.getenv("OPENAI_SECRET_KEY"))
        
         # Pega a última mensagem do usuário
        user_input = tracker.latest_message.get("text")

        # Cria a requisição para o ChatGPT
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente educacional da Universidade Metodista de Angola."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=150
            )

            reply = response.choices[0].message.content
        except Exception as e:
            print(f"[ERRO OpenAI] {str(e)}")
            reply = "Desculpe, houve um problema ao tentar responder. Pode reformular sua pergunta?"

        dispatcher.utter_message(text=reply)
        return []
        

# ✅ Verificar quais ações foram registradas
# if __name__ == "__main__" or True:  # Garante execução no Docker
print("📦 Verificando ações registradas:")
for cls in Action.__subclasses__():
    try:
        print(f"➡️ {cls().name()}")
    except Exception as e:
        print(f"❌ Falha ao carregar {cls.__name__}: {e}")


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
