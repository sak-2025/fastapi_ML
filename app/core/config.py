import os
from dotenv import load_dotenv

# load env var
load_dotenv()


class Settings:
    API_KEY=os.getenv('API_KEY','key')
    REDIS_URL=os.getenv('REDIS_URL','key')
    JWT_ALGORITHM='HS256'
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY','secret')
    MODEL_PATH ='app/models/model.pkl'


setting = Settings()
