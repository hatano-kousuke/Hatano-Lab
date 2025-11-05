from flask import Flask, render_template, request, redirect, url_for, flash

# SQLAlchemyとMigrateのインポートはそのまま
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flaskアプリの作成
app = Flask(__name__)

# ★ SECRET_KEYを追加: flashメッセージやセッションに必要です
app.config['SECRET_KEY'] = 'a_very_secret_key_for_flash' # 実際には.envから読み込むべきです

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
    # 必要に応じて他のモデルをここにインポート・定義してください

# --- ダミー記事データ (開発用) ---
# 実際にはデータベースから取得します
DUMMY_POSTS = [
    {'id': 1, 'title': 'FlaskとPostgreSQLで環境構築を行う手順', 'date': '2025-10-01', 'summary': '環境構築で躓いたポイントと解決策をまとめました。'},
    {'id': 2, 'title': 'SQLAlchemyのマイグレーション入門', 'date': '2025-10-15', 'summary': 'Flask-Migrateを使ったスキーマ管理の基本を解説。'},
    {'id': 3, 'title': 'Pythonでの非同期処理入門', 'date': '2025-11-01', 'summary': 'async/awaitを用いたWebスクレイピングの事例紹介。'},
]
# ---------------------------------

@app.route("/")
def top():
    # index.htmlにダミー記事一覧データを渡す
    return render_template('index.html', posts=DUMMY_POSTS)

# --- 記事詳細画面へのルート ---
# /post/1, /post/2 のようなURLに対応
@app.route("/post/<int:post_id>")
def post_detail(post_id):
    # DUMMY_POSTSから該当する記事を探す (本番ではDB検索)
    post = next((p for p in DUMMY_POSTS if p['id'] == post_id), None)
    
    if post is None:
        # 記事が見つからなかった場合の処理 (例: 404エラーページ)
        return render_template('404.html'), 404
        
    return render_template('post_detail.html', post=post)

# --- お問い合わせ画面へのルート ---
# /contact URLに対応
@app.route("/contact")
def contact():
    # お問い合わせ画面をレンダリングする
    return render_template('contact.html')

# --- ログイン画面へのルート (GET: 画面表示, POST: ログイン処理) ---
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        
        # 認証ロジックのダミー実装 (★管理者のみ許可)
        # ユーザーIDが 'admin'、パスワードが 'password' の場合のみ成功とする
        if user_id == 'admin' and password == 'password':
            # ログイン成功
            # 記事一覧画面（トップ画面）にリダイレクト
            flash('管理者としてログインに成功しました。', 'success')
            return redirect(url_for('top'))
        else:
            # ログイン失敗
            # flashメッセージを設定し、入力内容を保持してログイン画面に戻る
            flash('ユーザーIDまたはパスワードが正しくありません。', 'danger')
            # 入力内容を保持してテンプレートを再表示
            return render_template('login.html', user_id=user_id, password=password)
            
    # GETリクエスト（初期表示）の場合
    return render_template('login.html')


# Flaskアプリ起動用
if __name__ == "__main__":
    app.run(debug=True)