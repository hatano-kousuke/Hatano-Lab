from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from flask import session
from functools import wraps

# -----------------------------
# Flaskアプリ初期化
# -----------------------------
# run.py がルートにあり、テンプレートと静的ファイルが 'app/' ディレクトリ内にあるため、
# template_folder と static_folder を明示的に指定します。
app = Flask(__name__,
            template_folder='app/templates', # 16行目: テンプレートフォルダの場所を修正
            static_folder='app/static')     # 17行目: 静的フォルダの場所を修正
app.config["SECRET_KEY"] = "a_very_secret_key_for_flash"

# 画像アップロード設定
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
# 静的ファイルパスの構成を修正: app/static/uploads
UPLOAD_FOLDER = os.path.join(app.root_path, "app", "static", "uploads") 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    """許可された拡張子か判定"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# -----------------------------
# 管理者ログイン情報（固定）
# -----------------------------
ADMIN_ID = "admin"
ADMIN_PASSWORD = "pass123"


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
class User(db.Model):
    __tablename__ = "USR000"

    usr_id = db.Column(db.String(50), primary_key=True) 
    usr_nm = db.Column(db.String(100), nullable=False)
    usr_strt_date = db.Column(db.Date, nullable=True) 
    usr_end_date = db.Column(db.Date, nullable=True)
    delt_flg = db.Column(db.Integer, default=0)

    rec_crtn_prg_id = db.Column(db.String(50))
    rec_crtn_usr_id = db.Column(db.String(50))
    rec_crtn_tmstmp = db.Column(db.DateTime)
    rec_upd_prg_id = db.Column(db.String(50))
    rec_upd_usr_id = db.Column(db.String(50))
    rec_upd_tmstmp = db.Column(db.DateTime)

    password_relation = db.relationship("UserPassword", backref="user", uselist=False)


class UserPassword(db.Model):
    __tablename__ = "USR001"

    usr_id = db.Column(db.String(50), db.ForeignKey("USR000.usr_id"), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    pw_upd_tmstmp = db.Column(db.DateTime)
    delt_flg = db.Column(db.Integer, default=0)

    rec_crtn_prg_id = db.Column(db.String(50))
    rec_crtn_usr_id = db.Column(db.String(50))
    rec_crtn_tmstmp = db.Column(db.DateTime)
    rec_upd_prg_id = db.Column(db.String(50))
    rec_upd_usr_id = db.Column(db.String(50))
    rec_upd_tmstmp = db.Column(db.DateTime)
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


class ContactCategory(db.Model):
    __tablename__ = "contact_categories"

    contact_category_id = db.Column(db.Integer, primary_key=True)
    contact_category_name = db.Column(db.String(100), nullable=False)
    deleted_flg = db.Column(db.SmallInteger, default=0, nullable=False)

    rec_crtn_prg_id = db.Column(db.String(50), nullable=False, default="SYSTEM")
    rec_crtn_user_id = db.Column(db.String(10), nullable=False, default="GUEST")
    rec_crtn_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    rec_upd_prg_id = db.Column(db.String(50), nullable=False, default="SYSTEM")
    rec_upd_user_id = db.Column(db.String(10), nullable=False, default="GUEST")
    rec_upd_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


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

    rec_crtn_prg_id = db.Column(db.String(50), nullable=False, default="SYSTEM")
    rec_crtn_user_id = db.Column(db.String(10), nullable=False, default="GUEST")
    rec_crtn_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    rec_upd_prg_id = db.Column(db.String(50), nullable=False, default="SYSTEM")
    rec_upd_user_id = db.Column(db.String(10), nullable=False, default="GUEST")
    rec_upd_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    category = db.relationship("ContactCategory", backref="contacts")

# -----------------------------
# ログイン必須デコレータ
def login_required(fn):
     @wraps(fn)
     def wrapper(*args, **kwargs):
         if "logged_in" not in session or not session["logged_in"]:
             flash("ログインが必要です。", "danger")
             return redirect(url_for("login"))
         return fn(*args, **kwargs)
     return wrapper


# -----------------------------
# ルーティング定義
# -----------------------------

# ---------------------------------------------
# ログイン処理
# ---------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # フォームキーを 'usr_id' と 'password' に修正 (login.html に合わせる)
        username = request.form.get("username")
        password_input = request.form.get("password")
        
        error_message = "ユーザーIDまたはパスワードが間違っています。"
        
        user = (
            db.session.query(User)
            .join(UserPassword, User.usr_id == UserPassword.usr_id)
            .filter(
                User.usr_id == username,
                User.delt_flg == 0,
                UserPassword.delt_flg == 0
            )
            .first()
        )

        if user is None:
            flash(error_message, "danger") 
            return render_template("login.html")

        if user.password_relation.password != password_input:
            flash(error_message, "danger") 
            return render_template("login.html")

        # ログイン成功処理
        session["logged_in"] = True
        session["user_id"] = user.usr_id
        session["user_name"] = user.usr_nm

        flash(f"ようこそ {user.usr_nm} さん。", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("login.html")

# ---------------------------------------------
# ログアウト処理
# ---------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("ログアウトしました。", "info")
    return redirect(url_for("top"))


# -----------------------------
# トップページ（記事一覧）
# -----------------------------
@app.route("/")
def top():
    posts = Article.query.order_by(Article.article_id.desc()).all()
    return render_template(
        "index.html",
        posts=posts,
        logged_in=session.get("logged_in", False)
    )


# -----------------------------
# 記事詳細ページ
# -----------------------------
@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = Article.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)


# -----------------------------
# 記事作成（画像アップロード対応）
# -----------------------------
@app.route("/admin/post_create", methods=["GET", "POST"])
@login_required # 管理者機能にはデコレータを追加
def post_create():

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        image_file = request.files.get("image")

        if not title or not content:
            flash("タイトルと内容は必須です。", "danger")
            return redirect(url_for("post_create"))

        image_path = None

        # 画像保存処理
        if image_file and allowed_file(image_file.filename):
            original_filename = secure_filename(image_file.filename)

            # 重複防止のため uuid を付与
            ext = original_filename.rsplit(".", 1)[1].lower()
            unique_name = f"{uuid.uuid4().hex}.{ext}"

            save_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
            image_file.save(save_path)

            # static からの相対パスを保存
            image_path = f"uploads/{unique_name}"

        new_article = Article(
            article_title=title,
            article_body=content,
            article_image_path=image_path,
            deleted_flg=0,
            # ログインユーザーのIDを使用
            rec_crtn_user_id=session.get("user_id", "ADMIN"),
            rec_upd_user_id=session.get("user_id", "ADMIN"),
            rec_crtn_prg_id="admin_post_create",
            rec_upd_prg_id="admin_post_create",
        )

        db.session.add(new_article)
        db.session.commit()

        flash(f"記事『{title}』を作成しました。", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("post_create.html")


# -----------------------------
# 管理者ダッシュボード
# -----------------------------
@app.route("/admin/dashboard")
@login_required # 管理者機能にはデコレータを追加
def admin_dashboard():
    posts = Article.query.order_by(Article.article_id.desc()).all()
    contacts = Contact.query.order_by(Contact.contact_id.desc()).all()
    return render_template("admin_dashboard.html", posts=posts, contacts=contacts)


# -----------------------------
# お問い合わせフォーム表示
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
    category_name = request.form.get("category")
    content = request.form.get("contact_content")

    if not name or not email or not content or not category_name:
        flash("必須項目が未入力です。", "danger")
        return redirect(url_for("contact"))

    # カテゴリ名から contact_category_id を取得
    category = ContactCategory.query.filter_by(
        contact_category_name=category_name,
        deleted_flg=0
    ).first()

    # DBに存在しなければ新規作成
    if not category:
        category = ContactCategory(contact_category_name=category_name)
        db.session.add(category)
        db.session.commit()
        db.session.refresh(category) # IDを取得するためにリフレッシュ

    new_contact = Contact(
        contact_name=name,
        contact_furigana=furigana,
        contact_email=email,
        contact_category_id=category.contact_category_id,
        contact_content=content,
        contact_age=request.form.get("age"),
        contact_postal_code=request.form.get("postal"),
        contact_prefecture=request.form.get("prefecture"),
        contact_address=request.form.get("address"),
        contact_phone=request.form.get("phone"),
        rec_crtn_prg_id="contact_submit",
        rec_upd_prg_id="contact_submit",
    )

    db.session.add(new_contact)
    db.session.commit()

    flash("お問い合わせを送信しました。", "success")
    return render_template("contact_complete.html", form_data=request.form)


# -----------------------------
# お問い合わせ一覧（管理者用）
# -----------------------------
@app.route("/admin/contact_list")
@login_required # 管理者機能にはデコレータを追加
def contact_list():

    contacts = Contact.query.order_by(Contact.contact_id.desc()).all()
    return render_template("contact_list.html", contacts=contacts)


# -----------------------------
# 問い合わせ詳細表示エンドポイント
# -----------------------------
@app.route("/admin/contact_detail/<int:contact_id>")
@login_required
def contact_detail(contact_id):
    """
    特定の contact_id に基づいて問い合わせ詳細を表示するエンドポイント。
    """
    # contact_id を使ってデータベースから問い合わせの詳細を取得
    contact = Contact.query.get_or_404(contact_id)
    
    # 詳細表示用のテンプレートをレンダリング
    return render_template("contact_detail.html", contact=contact)


# -----------------------------
# 起動処理
# -----------------------------
def initialize_database(): # 353行目: データベース初期化関数の定義を開始
    """
    アプリケーションコンテキスト内で実行される初期化処理。
    テーブル作成と初期管理者ユーザーの投入を行います。
    """
    db.create_all()
    
    # 管理者ユーザーが存在するか確認
    admin_user = User.query.filter_by(usr_id=ADMIN_ID).first()
    
    if not admin_user:
        print(f"--- 初期管理者ユーザー '{ADMIN_ID}' を作成します ---")

        # USR000 (User) への挿入
        new_user = User(
            usr_id=ADMIN_ID,
            usr_nm="管理者",
            usr_strt_date=datetime.now().date(),
            delt_flg=0,
            rec_crtn_prg_id="INIT_SCRIPT",
            rec_crtn_usr_id="SYSTEM",
            rec_crtn_tmstmp=datetime.utcnow(),
            rec_upd_prg_id="INIT_SCRIPT",
            rec_upd_usr_id="SYSTEM",
            rec_upd_tmstmp=datetime.utcnow(),
        )
        db.session.add(new_user)

        # USR001 (UserPassword) への挿入
        new_password = UserPassword(
            usr_id=ADMIN_ID,
            password=ADMIN_PASSWORD,
            pw_upd_tmstmp=datetime.utcnow(),
            delt_flg=0,
            rec_crtn_prg_id="INIT_SCRIPT",
            rec_crtn_usr_id="SYSTEM",
            rec_crtn_tmstmp=datetime.utcnow(),
            rec_upd_prg_id="INIT_SCRIPT",
            rec_upd_usr_id="SYSTEM",
            rec_upd_tmstmp=datetime.utcnow(),
        )
        db.session.add(new_password)

        db.session.commit()
        print(f"--- 初期管理者ユーザーの作成が完了しました (ID: {ADMIN_ID}, PW: {ADMIN_PASSWORD}) ---")
    else:
        print(f"--- 管理者ユーザー '{ADMIN_ID}' は既に存在しています。---")


if __name__ == "__main__":
    with app.app_context():
        # 起動時にデータベースの初期化（テーブル作成と初期ユーザー投入）を実行
        initialize_database() # 399行目から402行目: 起動ロジックを修正し、重複したインポートを削除
    app.run(debug=True)