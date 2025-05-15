import yaml
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

CONFIG_PATH = "config/config.yaml"

def get_config():
    with open(CONFIG_PATH, "r") as f:
        raw_config = yaml.safe_load(f)

    # Inject secrets from .env
    raw_config["reddit"] = {
        "client_id": os.getenv("REDDIT_CLIENT_ID"),
        "client_secret": os.getenv("REDDIT_CLIENT_SECRET"),
        "user_agent": os.getenv("REDDIT_USER_AGENT"),
        "username": os.getenv("REDDIT_USERNAME"),      # Added
        "password": os.getenv("REDDIT_PASSWORD"),      # Added
    }

    raw_config["openai"]["api_key"] = os.getenv("OPENAI_API_KEY")

    return raw_config
