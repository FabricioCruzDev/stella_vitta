from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # O Pydantic buscará automaticamente uma variável com este nome no arquivo .env
    DATABASE_URL: str
    SECRET_KEY: str
    
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

try:
    settings = Settings()
except Exception as e:
    print("❌ Erro: Verifique se o arquivo .env existe e contém as variáveis necessárias.")
    raise e