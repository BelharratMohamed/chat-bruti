import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    # Model Configuration
    # Model Configuration
    HF_BASE_URL = os.environ.get("HF_BASE_URL", "https://router.huggingface.co/v1")
    HF_API_KEY = os.environ.get("HF_API_KEY") # Must be set in environment
    MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')
