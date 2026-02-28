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
    
    @property
    def sqlalchemy_track_modifications(self) -> bool:
        """
        Desactiva el sistema de seguimiento de modificaciones de SQLAlchemy.
        Ahorra memoria y recursos. Recomendado: False
        """
        return os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'
    
    @property
    def database_echo(self) -> bool:
        """
        Si True, SQLAlchemy imprime todas las queries SQL en la consola.
        Útil para debugging. Recomendado: True en desarrollo, False en producción.
        """
        return os.getenv('DATABASE_ECHO', 'False').lower() == 'true'
    

    #Api Congiguration
    @property
    def api_host(self) -> str:
        return os.getenv('API_HOST')
    
    @property
    def api_port(self) -> int:
        return int(os.getenv('API_PORT'))
    
    @property
    def app_debug(self) -> bool:
        return os.getenv('APP_DEBUG').lower() == 'true'
    
    #JWToken
    @property
    def JW_TOKEN_EXPIRATION_TIME(self) -> int:
        return int(os.getenv('JWT_EXPIRATION_TIME'))
    
    @property
    def JW_ALGORITHM(self) -> str:
        return os.getenv('JWT_ALGORITHM')
    
    @property
    def JW_SECRET_KEY(self) -> str:
        return os.getenv('SECRET_KEY')

    

config = Settings()
