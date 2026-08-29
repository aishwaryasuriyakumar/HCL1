from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    app_name: str = "LearnPath AI"
    app_env: str = "development"
    database_url: str = "sqlite:///./learnpath.db"
    frontend_url: str = "http://localhost:5173"
    llm_api_key: str = ""
    llm_model: str = ""
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.6-flash"

    @property
    def effective_gemini_api_key(self) -> str:
        return self.gemini_api_key or self.llm_api_key

    @property
    def effective_gemini_model(self) -> str:
        return self.gemini_model or self.llm_model or "gemini-3.6-flash"

    youtube_api_key: str = ""
    resource_verification_ttl_days: int = 7
    trusted_official_doc_domains: List[str] = [
        "python.org",
        "docs.python.org",
        "developer.mozilla.org",
        "huggingface.co",
        "developers.google.com",
        "docs.aws.amazon.com",
        "learn.microsoft.com",
        "pytorch.org",
        "tensorflow.org",
        "scikit-learn.org",
        "pandas.pydata.org",
        "numpy.org"
    ]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
