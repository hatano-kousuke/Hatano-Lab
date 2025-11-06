# Hatano-Lab/run.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flaskアプリの作成
app = Flask(__name__)

# ★ SECRET_KEY: flashメッセージに必要
app.config['SECRET_KEY'] = 'a_very_secret_key_for_flash'

# PostgreSQL設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kousuke8617@localhost/hatano_lab_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DBとマイグレーション設定
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- モデル定義（確認用） ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
# -----------------------------

# --- ダミー記事データ ---
DUMMY_POSTS = [
    {'id': 1, 'title': 'FlaskとPostgreSQLで環境構築を行う手順', 'date': '2025-10-01', 'summary': '環境構築で躓いたポイントと解決策をまとめました。'},
    {'id': 2, 'title': 'SQLAlchemyのマイグレーション入門', 'date': '2025-10-15', 'summary': 'Flask-Migrateを使ったスキーマ管理の基本を解説。'},
    {'id': 3, 'title': 'Pythonでの非同期処理入門', 'date': '2025-11-01', 'summary': 'async/awaitを用いたWebスクレイピングの事例紹介。'},
]
# ---------------------------

# --- 疑似ログイン状態 ---
logged_in = False  # ← 本来は session で管理すべき（今回は簡易実装）
# ---------------------------

# --- トップページ ---
@app.route("/")
def top():
    return render_template('index.html', posts=DUMMY_POSTS)

# --- お問い合わせページ ---
@app.route("/contact")
def contact():
    return render_template('contact.html')


# --- 記事編集ページ（ダミー実装） ---
@app.route("/admin/post_edit/<int:post_id>", methods=["GET", "POST"])
def post_edit(post_id):
    check = login_required()
    if check:
        return check  # 未ログイン時はログイン画面へリダイレクト

    post = next((p for p in DUMMY_POSTS if p['id'] == post_id), None)
    if post is None:
        flash("指定された記事が見つかりません。", "danger")
        return redirect(url_for("admin_posts"))

    if request.method == "POST":
        # 現時点ではDB更新せず、ダミー処理
        title = request.form.get("title")
        content = request.form.get("content")
        flash(f"『{title}』を更新しました。（仮）", "success")
        return redirect(url_for("post_detail", post_id=post_id))

    # GETリクエスト時（編集フォームを表示）
    return render_template("post_edit.html", post_id=post_id, post=post)

# --- 記事詳細ページ ---
@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in DUMMY_POSTS if p['id'] == post_id), None)
    if post is None:
        flash("指定された記事が見つかりません。", "danger")
        return redirect(url_for("top"))

    # logged_in をテンプレートに渡す（ログイン状態で表示を変えるため）
    return render_template("post_detail.html", post=post, logged_in=logged_in)


# --- 疑似ログインチェック関数 ---
def login_required():
    global logged_in
    if not logged_in:
        flash("このページを表示するにはログインが必要です。", "danger")
        return redirect(url_for('login'))
    return None

# --- 管理者用記事一覧 ---
@app.route("/admin/posts")
def admin_posts():
    check = login_required()
    if check:
        return check  # ログインしていない場合は /login にリダイレクト

    # ログイン済みなら記事管理画面を表示
    return render_template('admin_dashboard.html', posts=DUMMY_POSTS)

# --- ダミーログインページ ---
@app.route("/login", methods=["GET", "POST"])
def login():
    global logged_in  # ← 追加（ログイン状態の更新に使う）

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ダミーログインチェック（仮）
        if username == "admin" and password == "password":
            logged_in = True  # ← ログイン状態を更新
            flash("ログインに成功しました！", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("ユーザー名またはパスワードが間違っています。", "danger")
            return redirect(url_for("login"))

    # GETメソッド時：ログインフォームを表示
    return render_template("login.html")

# --- 管理者ダッシュボード ---
@app.route("/admin/dashboard")
def admin_dashboard():
    # 仮のデータ（データベース未使用）
    posts = [
        {"id": 1, "title": "Flaskアプリ初期構築", "date": "2025-11-01"},
        {"id": 2, "title": "SQLAlchemyの使い方入門", "date": "2025-11-02"},
        {"id": 3, "title": "Jinjaテンプレートで動的表示", "date": "2025-11-03"},
    ]
    return render_template("admin_dashboard.html", posts=posts)

# --- ログアウト処理（ダミー） ---
@app.route("/logout")
def logout():
    flash("ログアウトしました。", "info")
    return redirect(url_for("top"))


# --- Flaskアプリ起動 ---
if __name__ == "__main__":
    app.run(debug=True)
