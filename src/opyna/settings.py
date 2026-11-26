"""Configuración centralizada vía variables de entorno (.env)."""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # rutas
    data_dir: Path = Path("./data")

    # modelos
    model_absa: str = "yangheng/deberta-v3-base-absa-v1.1"

    # claves (opcionales en desarrollo)
    openai_api_key: str | None = None
    telegram_bot_token: str | None = None

    log_level: str = "INFO"

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def processed_dir(self) -> Path:
        return self.data_dir / "processed"


settings = Settings()
