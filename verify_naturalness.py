import json
import random
import sys
import os

# Add current directory to path to import app
sys.path.append(os.getcwd())

from app import Brain

def verify_naturalness():
    print("Initializing Brain...")
    brain = Brain()
    
    forbidden_words = [
        "algorithme", "robot", "binaire", "cortex", "processeur", "données", 
        "entité", "carbonée", "humain", "système", "variable", "fonction", 
        "exception", "module", "téléchargement", "mise à jour"
    ]
    
    test_inputs = [
        "Bonjour", "Qui es-tu ?", "Tu es nul", "Tu es super", "Pourquoi ?", 
        "Raconte une histoire", "Je t'aime", "Connard", "Aide moi", 
        "Quelle heure est-il ?", "Quel jour on est ?", "Quel temps fait-il ?", 
        "Combien font 2+2", "Parle moi de Linux", "C'est quoi Windows", 
        "J'aime les chats", "La vie est belle", "Je joue à Fortnite"
    ]
    
    iterations = 1000
    failures = 0
    
    print(f"Running {iterations} tests...")
    
    for i in range(iterations):
        user_input = random.choice(test_inputs)
        # Mock context
        context = {'last_topic': None, 'last_intent': None}
        response = brain.generate_response(user_input, context, request_count=i)
        
        response_lower = response.lower()
        
        for word in forbidden_words:
            if word in response_lower:
                print(f"FAILURE: Found forbidden word '{word}' in response: '{response}'")
                failures += 1
                
    if failures == 0:
        print(f"SUCCESS: {iterations} tests passed. No robotic words found.")
    else:
        print(f"FAILURE: {failures} responses contained robotic words.")
        sys.exit(1)

if __name__ == "__main__":
    verify_naturalness()
