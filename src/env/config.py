from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    ENV: str = os.getenv("ENV")

    DATABASE_URL: str = (
        f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

settings = Settings()
