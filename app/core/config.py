import os

from attr import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

settings = Settings()