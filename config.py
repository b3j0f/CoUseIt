class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    TEST = False
    SECRET_KEY = 'TO CHANGE'
    EXCLUDE = []  #: modules to not load

    SQLALCHEMY_DATABASE_URI = 'postgresql://costockit:c0st0ck1t@localhost:5432/costockit'


class ProductionConfig(Config):
    EXCLUDE = ['test']


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    EXCLUDE = ['test']


class TestConfig(Config):
    TEST = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://costockit_test:costockit_test@localhost:5432/costockit_test'


configs = {
    'prod': ProductionConfig,
    'dev': DevelopmentConfig,
    'test': TestConfig
}

config = configs['dev']
