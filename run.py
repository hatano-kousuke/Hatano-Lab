from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flaskアプリの作成
app = Flask(__name__)

# PostgreSQL設定（A5SQLでも同じDBに接続可能）
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kousuke8617@localhost/hatano_lab_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DBとマイグレーション設定
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# モデル定義例（マイグレーション確認用）
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

# Flaskアプリ起動用
if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def home():
    return "Hello, Flask!"