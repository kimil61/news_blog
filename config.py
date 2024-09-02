import os


class Config:
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess-aha'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app):
        cls.SECRET_KEY = os.environ.get('SECRET_KEY') or cls.SECRET_KEY
        cls.MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
        cls.MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
        cls.MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
        cls.MYSQL_DB = os.environ.get('MYSQL_DB', 'newsblog')

        cls.SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}@{cls.MYSQL_HOST}/{cls.MYSQL_DB}"

        app.config.from_object(cls)