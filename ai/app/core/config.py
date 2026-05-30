from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env.dev',
        extra='ignore',
        protected_namespaces=('settings_',),
    )

    app_env: str = 'development'
    app_name: str = 'SprintMind AI Service'
    app_host: str = '0.0.0.0'
    app_port: int = 8777
    app_version: str = '1.0.0'

    model_provider: str = 'mock'
    llm_model_name: str = 'mock-model'
    embedding_model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'

    openai_api_key: str = ''
    anthropic_api_key: str = ''
    gemini_api_key: str = ''

    request_timeout_seconds: int = 30
    max_retries: int = 2
    log_level: str = 'debug'


settings = Settings()
