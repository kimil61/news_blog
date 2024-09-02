import os

class Config:
    WTF_CSRF_ENABLED = True
    # SECRET_KEY = 'your-secret-key'  # 실제 운영 환경에서는 환경 변수에서 가져오는 것이 좋습니다.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-aha'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    