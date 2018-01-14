# config.py

## Created by James L. 06/07/2017


class Config(object):
    """
    Common configurations

    """
    MODE = 'local'

    ## common configurations here across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    TESTING = True
    SQL_ALCHEMY_ECHO = False



class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}