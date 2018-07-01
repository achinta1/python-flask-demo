import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    TESTING = False
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "szahjdgsahdfh34535@343@#$@##676"
    WTF_CSRF_SECRET_KEY = "szahjdgsahdfh34535@343@#$@##676"
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "db", 'app.db')
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://root:matrix@localhost/flask_demo'
    ALEMBIC_MIGRATE_DIR = os.path.join(basedir, "db", 'migrations')

class TestConfig(Config):
    # Disable error catching
    # TESTING = True
    # In-memory DB
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "szahjdgsahdfh34535@343@#$@##676"
    WTF_CSRF_SECRET_KEY = "szahjdgsahdfh34535@343@#$@##676"
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "db", 'app.db')
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://root:matrix@localhost/flask_demo'
    ALEMBIC_MIGRATE_DIR = os.path.join(basedir, "db", 'migrations')

class DevelopmentConfig(Config):
    TESTING = False
    DEBUG = True
    WTF_CSRF_ENABLED = True
    #-----App Debugger enable-------
    DEBUG_TB_INTERCEPT_REDIRECTS=False
    #DEBUG_TB_ENABLED=True
    #DEBUG_TB_HOSTS=True
    #DEBUG_TB_PANELS=True
    DEBUG_TB_PROFILER_ENABLED=True
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED=True
    #----- ./ App Debugger enable-------
    SECRET_KEY = "szahjdgsahdfh34535@343@#$@##676"
    WTF_CSRF_SECRET_KEY = "szahjdgsahdfh34535@343@#$@##676"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "db", 'app.db')
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://root:matrix@localhost/flask_demo'
    ALEMBIC_MIGRATE_DIR = os.path.join(basedir, "db", 'migrations')