# Hatano-Lab/run.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

# -----------------------------
# Flaskアプリ初期化
# -----------------------------
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.config["SECRET_KEY"] = "a_very_secret_key_for_flash"

# -----------------------------
# DB設定
# -----------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:kousuke8617@localhost/hatano_lab_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# -----------------------------
# モデル定義
# -----------------------------

# --- ユーザーテーブル（USR000） ---
class User(db.Model):
    __tablename__ = "usr000"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


# --- 記事テーブル ---
class Article(db.Model):
    __tablename__ = "articles"
    article_id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(200), nullable=False)
    article_body = db.Column(db.Text, nullable=False)
    article_image_path = db.Column(db.String(255))
    deleted_flg = db.Column(db.SmallInteger, nullable=False, default=0)
    rec_crtn_user_id = db.Column(db.String(50))
    rec_upd_user_id = db.Column(db.String(50))
    rec_crtn_prg_id = db.Column(db.String(50))
    rec_upd_prg_id = db.Column(db.String(50))
    rec_crtn_tmstmp = db.Column(db.DateTime, default=datetime.utcnow)
    rec_upd_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# --- お問い合わせ区分（CTU001） ---
class ContactCategory(db.Model):
    __tablename__ = "contact_categories"

    contact_category_id = db.Column(db.Integer, primary_key=True)
    contact_category_name = db.Column(db.String(100), nullable=False)
    deleted_flg = db.Column(db.SmallInteger, default=0, nullable=False)

    rec_crtn_prg_id = db.Column(db.String(50), nullable=False, default='SYSTEM')
    rec_crtn_user_id = db.Column(db.String(10), nullable=False, default='GUEST')
    rec_crtn_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    rec_upd_prg_id = db.Column(db.String(50), nullable=False, default='SYSTEM')
    rec_upd_user_id = db.Column(db.String(10), nullable=False, default='GUEST')
    rec_upd_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# --- お問い合わせ情報（CTU000） ---
class Contact(db.Model):
    __tablename__ = "contacts"

    contact_id = db.Column(db.Integer, primary_key=True)
    contact_category_id = db.Column(db.Integer, db.ForeignKey("contact_categories.contact_category_id"))
    contact_content = db.Column(db.Text, nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_furigana = db.Column(db.String(100))
    contact_email = db.Column(db.String(255), nullable=False)
    contact_age = db.Column(db.Integer)
    contact_postal_code = db.Column(db.String(20))
    contact_prefecture = db.Column(db.String(50))
    contact_address = db.Column(db.String(255))
    contact_phone = db.Column(db.String(20))
    replied_flg = db.Column(db.SmallInteger, default=0, nullable=False)
    deleted_flg = db.Column(db.SmallInteger, default=0, nullable=False)

    rec_crtn_prg_id = db.Column(db.String(50), nullable=False, default='SYSTEM')
    rec_crtn_user_id = db.Column(db.String(10), nullable=False, default='GUEST')
    rec_crtn_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    rec_upd_prg_id = db.Column(db.String(50), nullable=False, default='SYSTEM')
    rec_upd_user_id = db.Column(db.String(10), nullable=False, default='GUEST')
    rec_upd_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    category = db.relationship("ContactCategory", backref="contacts")


# -----------------------------
# 疑似ログイン制御
# -----------------------------
logged_in = True  # デモ用（常にログイン状態）

def login_required():
    global logged_in
    if not logged_in:
        flash("このページを表示するにはログインが必要です。", "danger")
        return redirect(url_for("login"))
    return None


# -----------------------------
# ログイン・ログアウト
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    global logged_in
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "password":
            logged_in = True
            flash("ログインしました。", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("ユーザー名またはパスワードが違います。", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    global logged_in
    logged_in = False
    flash("ログアウトしました。", "info")
    return redirect(url_for("top"))


# -----------------------------
# トップページ（記事一覧）
# -----------------------------
@app.route("/")
def top():
    posts = Article.query.order_by(Article.article_id.desc()).all()
    return render_template("index.html", posts=posts, logged_in=logged_in)


# -----------------------------
# 記事詳細ページ（★追加）
# -----------------------------
@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = Article.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post, logged_in=logged_in)


# -----------------------------
# 記事作成
# -----------------------------
@app.route("/admin/post_create", methods=["GET", "POST"])
def post_create():
    check = login_required()
    if check:
        return check

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        image = request.files.get("image")

        if not title or not content:
            flash("タイトルと内容は必須です。", "danger")
            return redirect(url_for("post_create"))

        image_path = None
        if image and image.filename != "":
            upload_dir = os.path.join(app.static_folder, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            image_path = os.path.join("uploads", image.filename)
            image.save(os.path.join(app.static_folder, image_path))

        new_article = Article(
            article_title=title,
            article_body=content,
            article_image_path=image_path,
            deleted_flg=0,
            rec_crtn_user_id="ADMIN",
            rec_upd_user_id="ADMIN",
            rec_crtn_prg_id="admin_post_create",
            rec_upd_prg_id="admin_post_create",
        )
        db.session.add(new_article)
        db.session.commit()
        flash(f"記事『{title}』を作成しました。", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("post_create.html", logged_in=logged_in)


# -----------------------------
# 管理者ダッシュボード
# -----------------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    check = login_required()
    if check:
        return check

    posts = Article.query.order_by(Article.article_id.desc()).all()
    contacts = Contact.query.order_by(Contact.contact_id.desc()).all()
    return render_template("admin_dashboard.html", posts=posts, contacts=contacts, logged_in=logged_in)


# -----------------------------
# お問い合わせページ
# -----------------------------
@app.route("/contact", methods=["GET"])
def contact():
    categories = ContactCategory.query.filter_by(deleted_flg=0).all()
    return render_template("contact.html", categories=categories)


@app.route("/contact/submit", methods=["POST"])
def contact_submit():
    name = request.form.get("contact_name")
    furigana = request.form.get("contact_furigana")
    email = request.form.get("contact_email")
    category_id = request.form.get("contact_category_id")
    content = request.form.get("contact_content")

    if not name or not email or not content:
        flash("必須項目が未入力です。", "danger")
        return redirect(url_for("contact"))

    new_contact = Contact(
        contact_name=name,
        contact_furigana=furigana,
        contact_email=email,
        contact_category_id=category_id,
        contact_content=content,
        rec_crtn_prg_id="contact_submit",
        rec_upd_prg_id="contact_submit",
    )
    db.session.add(new_contact)
    db.session.commit()

    flash("お問い合わせを送信しました。", "success")
    return render_template("contact_complete.html", form_data=request.form)

# お問い合わせ一覧（管理者用）
# -----------------------------
@app.route("/admin/contact_list")
def contact_list():
    check = login_required()
    if check:
        return check

    contacts = Contact.query.order_by(Contact.contact_id.desc()).all()
    return render_template("contact_list.html", contacts=contacts, logged_in=logged_in)

# -----------------------------
# 起動処理
# -----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
