import os
from pathlib import Path
from dotenv import load_dotenv

class Settings:
    def __init__(self, env_file: str = 'enviroments/enviroment.env'):
        env_path = Path('.') / env_file    
        if not env_path.exists():            
            raise FileNotFoundError(
                f"Archivo de configuración no encontrado: {env_path.absolute()}\n"
                f"Por favor, crea el archivo '{env_file}' en el directorio raíz del proyecto."
            )    
        load_dotenv(env_path)        
    
    def model_path(self) -> str:
        return os.getenv('APP_MODEL_PATH')
    
    def corpus_esp_path(self) -> str:
        return os.getenv('CORPUS_ESP_PATH')
    
    def corpus_yor_path(self) -> str:
        return os.getenv('CORPUS_YOR_PATH')
    
    #Normalized corpus paths
    def corpus_esp_clean_path(self) -> str:
        return os.getenv('CORPUS_ESP_CLEAN_PATH')
    
    def corpus_yor_clean_path(self) -> str:
        return os.getenv('CORPUS_YOR_CLEAN_PATH')
    
    #DataBase
    @property
    def database_url(self) -> str:                     
        return os.getenv('DATABASE_URL')
    

    #Api Congiguration
    @property
    def api_host(self) -> str:
        return os.getenv('API_HOST', '0.0.0.0')
    
    @property
    def api_port(self) -> int:
        return int(os.getenv('API_PORT', '5000'))
    
    @property
    def app_debug(self) -> bool:
        return os.getenv('APP_DEBUG', 'False').lower() == 'true'
    

config = Settings()
