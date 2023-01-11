import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_NAME = "remember_to_buy"
    DESCRIPTION = (
        "Remember To Buy REST API. Repository: [GITHUB](https://github.com/blasmoyano/remember_to_buy)."
        " Use this API CRUD for Items."
    )
    API_V1_STR: str = "/api/v1.0"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    IS_TEST = os.environ.get("IS_TEST", False)

    # SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    # SQLALCHEMY_DATABASE_URL = "postgresql://REMEMBER:REMEMBER@postgresserver/REMEMBER"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DB_NAME: str
    DB_USER: str
    DB_PASSW: str
    DB_HOST: str
    DB_PORT: str
    if IS_TEST:
        SQLALCHEMY_DATABASE_URI: str = None
    else:
        SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

        @validator("SQLALCHEMY_DATABASE_URI", pre=True)
        def assemble_db_connection(
            cls, v: Optional[str], values: Dict[str, Any]
        ) -> Any:
            if isinstance(v, str):
                return v

            return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("DB_USER"),
                password=values.get("DB_PASSW"),
                host=values.get("DB_HOST"),
                port=values.get("DB_PORT"),
                path=f"/{values.get('DB_NAME') or ''}",
            )

    class Config:
        case_sensitive = True


settings = Settings()
