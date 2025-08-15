
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URI: str
    ECHO_SQL: bool

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / "config/local.env",
        # 如果需要使用环境变量文件，可以取消下面的注释 import os
        # env_file=Path(__file__).parent / "config" / os.getenv("APP_ENV_FILE", "local.env"),
        case_sensitive=True,
    )


settings = Settings.model_validate({})
if __name__ == '__main__':
    print(settings.model_dump_json(indent=2))
    print(f"DB_URI: {settings.DB_URI}")
    print(f"ECHO_SQL: {settings.ECHO_SQL}")