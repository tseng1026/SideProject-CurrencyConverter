import os

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    # Environment Variables
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    SERVER_NAME: str = os.getenv("SERVER_NAME")
    SERVER_HOST: AnyHttpUrl = os.getenv("SERVER_HOST")
    API_PREFIX: str = os.getenv("API_PREFIX")
    STATIC_FILE: str = os.getenv("STATIC_FILE")

    # Iso Crawler Coonfigs
    ISO_CRAWLER_STR: str = os.getenv("ISO_CRAWLER_STR")

    # Visa API Configs
    VISA_API_STR: str = os.getenv("VISA_API_STR")
    VISA_SSL_CERT: str = os.getenv("VISA_SSL_CERT")
    VISA_SSL_KEY: str = os.getenv("VISA_SSL_KEY")
    VISA_AUTH_USERNAME: str = os.getenv("VISA_AUTH_USERNAME")
    VISA_AUTH_PASSWORD: str = os.getenv("VISA_AUTH_PASSWORD")

    # MasterCard API Configs
    MASTERCARD_API_STR: str = os.getenv("MASTERCARD_API_STR")
    MASTERCARD_OPENSSL_KEY: str = os.getenv("MASTERCARD_OPENSSL_KEY")
    MASTERCARD_OPENSSL_PASSWORD: str = os.getenv("MASTERCARD_OPENSSL_PASSWORD")
    MASTERCARD_CONSUMER_KEY: str = os.getenv("MASTERCARD_CONSUMER_KEY")

    # YahooFinance Crawler Configs
    YAHOO_CRAWLER_STR: str = os.getenv("YAHOO_CRAWLER_STR")


load_dotenv()
settings = Settings()
