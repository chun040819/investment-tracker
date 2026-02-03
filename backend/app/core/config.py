from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application configuration pulled from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = f"sqlite:///{(BASE_DIR.parent / 'data' / 'app.db').as_posix()}"
    app_name: str = "Investment Tracker Backend"

    @staticmethod
    def _ensure_sqlite_dir(url: str) -> None:
        """Create directory for SQLite database if the URL points to a local file."""
        if url.startswith("sqlite:///"):
            db_path = Path(url.removeprefix("sqlite:///"))
        elif url.startswith("sqlite:////"):
            # absolute path form
            db_path = Path(url.removeprefix("sqlite:////")).resolve()
        else:
            return
        db_path.parent.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings._ensure_sqlite_dir(settings.database_url)
