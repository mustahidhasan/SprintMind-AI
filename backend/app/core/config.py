from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.dev", extra="ignore")

    app_env: str = "development"
    app_name: str = "SprintMind AI Backend"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str = ""
    frontend_url: str = "http://localhost:3000"

    jwt_secret: str = "change_me"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7
    encryption_key: str = "change_me_32_char_encryption_key"
    log_level: str = "debug"


settings = Settings()
