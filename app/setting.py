from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "pre-app"

    mongo_user: str = "user"
    mongo_password: str = "password"
    mongo_host: str = "localhost"
    mongo_port: str = "27017"
