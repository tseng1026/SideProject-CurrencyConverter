from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    # Environment Variables
    PROJECT_NAME: str = "Currency Converter"
    SERVER_NAME: str = "currency_converter"
    SERVER_HOST: AnyHttpUrl
    SERVER_PORT: int
    BASE_DIR: str
    STATIC_DIR: str
    API_PREFIX: str

    # Iso Crawler Coonfigs
    ISO_CRAWLER_STR: str
    ISO_CURRENCY_FILE: str

    # Visa API Configs (x-pay-token)
    VISA_API_STR: str
    VISA_API_KEY: str
    VISA_SHARED_SECRET: str

    # MasterCard API Configs (pkcs12 and dump private key)
    MASTERCARD_API_STR: str
    MASTERCARD_PRIVATE_KEY: str
    MASTERCARD_CONSUMER_KEY: str

    # YahooFinance Crawler Configs
    YAHOO_CRAWLER_STR: str

    class Config:
        env_file = ".env"


settings = Settings()
