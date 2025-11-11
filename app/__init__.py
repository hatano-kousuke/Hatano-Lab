# Hatano-Lab/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    # モデルを読み込む（テーブル定義を登録する）
    # モデルを読み込む（テーブル定義を登録する）
    from app.models import User, Password


    # ✅ ルーティング登録（Blueprintを読み込み）
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
