import os
from dotenv import load_dotenv

# Ek dum exact absolute path rule jo har folder environment se root ko trigger karega
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
env_path = os.path.join(BASE_DIR, '.env')

load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")