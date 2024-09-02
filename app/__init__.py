import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()
cache = Cache(config={'CACHE_TYPE': 'simple'})

# .env 파일 로드
load_dotenv()

## 개발환경에서만, 구글 로그인을 위한 설정. https 를 적용하면 이거 삭제해야 함.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)

    from app.views import main, auth, user, post, tag ,errors
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(post.bp)
    app.register_blueprint(tag.bp)
    app.register_blueprint(errors.bp)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/newsblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Newsblog startup')

    return app