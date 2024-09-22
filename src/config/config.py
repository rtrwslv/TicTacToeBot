"""Module for config."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    Attributes:
        POSTGRES_HOST (str): The hostname of the PostgreSQL database.
        POSTGRES_PORT (int): The port number of the PostgreSQL database.
        POSTGRES_USER (str): The username for the PostgreSQL database.
        POSTGRES_PASSWORD (str): The password for the PostgreSQL database.
        POSTGRES_DB (str): The name of the PostgreSQL database.
        API_HOST (str): The hostname of the API server.
        API_PORT (int): The port number of the API server.
        REDIS_HOST (str): The hostname of the Redis server.
        REDIS_PORT (int): The port number of the Redis server.
        REDIS_PASSWORD (str): The password for the Redis server.
        TELEGRAM_API_TOKEN (str): The API token for the Telegram bot.
    """

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def POSTGRES_URL(self) -> str:
        """
        Generate the PostgreSQL connection URL.

        This property method constructs the PostgreSQL connection URL based on
        the configured PostgreSQL settings.

        Returns:
            str: The PostgreSQL connection URL.
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}"
            f":{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    API_HOST: str
    API_PORT: int

    @property
    def API_URL(self) -> str:
        """
        Generate the API server URL.

        Returns:
            str: The API server URL.
        """
        return f"http://{self.API_HOST}:{self.API_PORT}"

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    TELEGRAM_API_TOKEN: str

    WEBHOOK_PORT: int
    WEBHOOK_DOMAIN: str
    JWT_SECRET: str


settings = Settings()
