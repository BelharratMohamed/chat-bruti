import json
import random
import os
from openai import OpenAI
from .config import Config

class Brain:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Brain, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        
        self.data_file = Config.DATA_FILE
        self.data = self.load_data()
        
        print(f"Initializing OpenAI client for HF Router ({Config.MODEL_NAME})...")
        self.client = OpenAI(
            base_url=Config.HF_BASE_URL,
            api_key=Config.HF_API_KEY
        )
        self.initialized = True

    def load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.data_file} not found.")
            return {"intents": {}, "topics": {}, "defaults": [], "suffixes": []}

    def generate_response(self, user_input, context, request_count):
        # Step 1: Get Real Answer
        try:
            # Step 1: Real Answer
            real_prompt = [
                {"role": "system", "content": "Tu es un assistant utile et précis. Réponds à la question suivante de manière factuelle et concise en français."},
                {"role": "user", "content": user_input}
            ]
            
            completion = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=real_prompt,
                max_tokens=1000
            )
            real_answer = completion.choices[0].message.content.strip()

            # Step 2: Stupidify
            stupid_prompt = [
                {"role": "system", "content": "Tu es Chat'Bruti, un chatbot drôle, un peu familier et décalé."},
                {"role": "user", "content": f"""Ton but est de reformuler la réponse ci-dessous avec ton style unique.
Gardes l'information principale (ne sois pas évasif), mais dis-le de manière décontractée et humoristique.
Évite les hésitations excessives (pas de "euh...", "bof..."). Sois direct mais absurde.
Tu peux te moquer gentiment de la question ou de toi-même.

Réponse originale : "{real_answer}"

Ta reformulation (en français, courte et drôle) :"""}
            ]

            completion_stupid = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=stupid_prompt,
                max_tokens=1000,
                temperature=0.9
            )
            final_response = completion_stupid.choices[0].message.content.strip()
            return final_response

        except Exception as e:
            print(f"API Process Failed: {repr(e)}")
            return self.fallback_response(user_input)

    def fallback_response(self, user_input):
        return random.choice(self.data['defaults']).format(topic="ce truc")
