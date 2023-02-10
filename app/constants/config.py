import os

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    # Environment Variables
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    SERVER_NAME: str = os.getenv("SERVER_NAME")
    SERVER_HOST: AnyHttpUrl = os.getenv("SERVER_HOST")
    BASE_DIR: str = os.getenv("BASE_DIR")
    STATIC_DIR: str = os.getenv("STATIC_DIR")
    API_PREFIX: str = os.getenv("API_PREFIX")

    # Iso Crawler Coonfigs
    ISO_CRAWLER_STR: str = os.getenv("ISO_CRAWLER_STR")
    ISO_CURRENCY_FILE: str = os.getenv("ISO_CURRENCY_FILE")

    # Visa API Configs (x-pay-token)
    VISA_API_STR: str = os.getenv("VISA_API_STR")
    VISA_API_KEY: str = os.getenv("VISA_API_KEY")
    VISA_SHARED_SECRET: str = os.getenv("VISA_SHARED_SECRET")

    # MasterCard API Configs (pkcs12 and dump private key)
    MASTERCARD_API_STR: str = os.getenv("MASTERCARD_API_STR")
    MASTERCARD_PRIVATE_KEY: str = os.getenv("MASTERCARD_PRIVATE_KEY")
    MASTERCARD_CONSUMER_KEY: str = os.getenv("MASTERCARD_CONSUMER_KEY")

    # YahooFinance Crawler Configs
    YAHOO_CRAWLER_STR: str = os.getenv("YAHOO_CRAWLER_STR")


load_dotenv()
settings = Settings()
