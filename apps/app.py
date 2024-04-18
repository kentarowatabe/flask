from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config
from flask_login import LoginManager #LoginManagerのインポート

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager() #LoginManagerのインスタンス化
login_manager.login_view = "auth.signup" #ログインしていない場合の行先
login_manager.login_message = "" #ログイン後のメッセージ

def create_app(config_key):
    app = Flask(__name__)
    app.config.from_object(config[config_key])

    csrf.init_app(app)
    db.init_app(app)
    Migrate(app,db)
    login_manager.init_app(app) #初期化
    
    from apps.crud import views as crud_views
    from apps.auth import views as auth_views #views.pyをauth_viewsという名前で読み込み
    from apps.detector import views as dt_views
    app.register_blueprint(crud_views.crud,url_prefix="/crud") 
    app.register_blueprint(auth_views.auth,url_prefix="/auth") #blueprintでauthアプリを登録
    app.register_blueprint(dt_views.dt)
    return app