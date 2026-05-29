from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.dev", extra="ignore")

    app_env: str = "development"
    app_name: str = "SprintMind AI Backend"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    database_url: str = ""
    ai_service_url: str = "http://localhost:8777/api/v1"
    frontend_url: str = "http://localhost:3000"

    jwt_secret: str = ""
    encryption_key: str = ""
    log_level: str = "info"


settings = Settings()
