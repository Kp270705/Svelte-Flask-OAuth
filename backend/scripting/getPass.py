import os
from dotenv import load_dotenv
from pathlib import Path

# Get root directory path (assuming this script is always run from root or you want absolute reference)
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

# Access environment variables
password1 = os.getenv("PASSWORD1")  
password2 = os.getenv("PASSWORD2") 
