from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    ip: str = "0.0.0.0"
    port: int = 8808
    base_saving_dir: str = os.path.join(os.getcwd(), 'saved')