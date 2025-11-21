from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Render will provide the full DB URL
    DATABASE_URL: str

    # other settings
    postgres_user: str
    postgres_password: str
    postgres_db: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )


settings = Settings()
