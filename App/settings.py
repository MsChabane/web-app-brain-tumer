from pydantic_settings import SettingsConfigDict ,BaseSettings


class Settings(BaseSettings):
    DATABASE_URL : str 
    JWT_SECRET: str
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )


setting = Settings()