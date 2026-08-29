from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "LearnPath AI"
    app_env: str = "development"
    database_url: str = "sqlite:///./learnpath.db"
    frontend_url: str = "http://localhost:5173"
    llm_api_key: str = ""
    llm_model: str = ""

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
