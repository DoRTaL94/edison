import secrets
import inspect
import sys, inspect


def get_config_object(env_keyword: str):
    """
    Returns the the desired config class path.

    The function iterates through a dictionary returned by inspect.
    The dictionary contains details about all of the file members.
    Its key is the name of the member and value is obj which contains all the details about the member.
    The desired config path is being picked by the ENV_KEYWORD field defined in the config class.

    Parameters:
    env_keyword (str): Should be equals to one of the config classes ENV_KEYWORD field.

    Returns:
    str: module_name.class_name, which is the full path of the config class.
    """
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if issubclass(obj, Config) and obj.ENV_KEYWORD == env_keyword:
            return ".".join([obj.__module__, name])


class Config:
    ENV_KEYWORD = ""
    DEBUG = False
    # Turns off the Flask-SQLAlchemy event system
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Turn off the Flask-SQLAlchemy event system
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Enables response message for unauthenticated requests
    PROPAGATE_EXCEPTIONS = True
    # This tells the JWTManager to use jwt.token_in_blacklist_loader callback
    JWT_BLACKLIST_ENABLED = True
    # JWTManager uses this secret key for creating tokens
    JWT_SECRET_KEY = secrets.token_hex(24)
    # We're going to check if both access_token and refresh_token are black listed
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:edison@127.0.0.1/edison'

# PostgreSQL connection string should be updated once an actual production environment is established.
class ProductionConfig(Config):
    ENV_KEYWORD = "production"


class DevelopmentConfig(Config):
    ENV_KEYWORD = "development"
    DEBUG = True

class TestConfig(Config):
    ENV_KEYWORD = "test"
    TESTING = True
