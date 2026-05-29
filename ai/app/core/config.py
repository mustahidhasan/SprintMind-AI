from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.dev", extra="ignore")

    app_name: str = "SprintMind AI Service"
    log_level: str = "info"


settings = Settings()
