from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def database_url(self) -> str:
        # return (
        #     f"postgres://{self.db_user}:{self.db_password}"
        #     f"@{self.db_host}:{self.db_port}/{self.db_name}"
        # )
        return (
                    f"postgres://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
                )

settings = Settings()