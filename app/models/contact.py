# Hatano-Lab/app/models/contact.py
from app import db  # Flask-SQLAlchemy の db インスタンス
from datetime import datetime

# ---------------------------
# お問い合わせ区分情報 (CTU001)
# ---------------------------
class ContactCategory(db.Model):
    __tablename__ = 'contact_categories'  # CTU001

    # 主キー
    id = db.Column('contact_category_id', db.Integer, primary_key=True)
    
    # 区分名称
    name = db.Column('contact_category_name', db.String(100), nullable=False)
    
    # 制御フラグ
    deleted_flg = db.Column(db.SmallInteger, default=0, nullable=False)
    
    # システム情報
    rec_crtn_prg_id = db.Column(db.String(50), nullable=False, default='SYSTEM')
    rec_crtn_user_id = db.Column(db.String(10), nullable=False, default='GUEST')
    rec_crtn_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    rec_upd_prg_id = db.Column(db.String(50), nullable=False, default='SYSTEM')
    rec_upd_user_id = db.Column(db.String(10), nullable=False, default='GUEST')
    rec_upd_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<ContactCategory {self.id}: {self.name}>'

# ---------------------------
# お問い合わせ情報 (CTU000)
# ---------------------------
class Contact(db.Model):
    __tablename__ = 'contacts'  # CTU000

    # 主キー
    id = db.Column('contact_id', db.Integer, primary_key=True)
    
    # 区分ID（外部キー）
    category_id = db.Column('contact_category_id', db.Integer, db.ForeignKey('contact_categories.contact_category_id'))
    category = db.relationship('ContactCategory', backref='contacts')
    
    # お問い合わせ内容
    content = db.Column('contact_content', db.Text, nullable=False)
    
    # 氏名・フリガナ・メールアドレスなど
    name = db.Column('contact_name', db.String(100), nullable=False)
    furigana = db.Column('contact_furigana', db.String(100), nullable=True)
    email = db.Column('contact_email', db.String(255), nullable=False)
    age = db.Column('contact_age', db.Integer, nullable=True)
    postal_code = db.Column('contact_postal_code', db.String(20), nullable=True)
    prefecture = db.Column('contact_prefecture', db.String(50), nullable=True)
    address = db.Column('contact_address', db.String(255), nullable=True)
    phone = db.Column('contact_phone', db.String(20), nullable=True)
    
    # 返信済フラグ
    replied_flg = db.Column('replied_flg', db.SmallInteger, default=0, nullable=False)
    
    # 削除フラグ
    deleted_flg = db.Column('deleted_flg', db.SmallInteger, default=0, nullable=False)
    
    # システム情報
    rec_crtn_prg_id = db.Column(db.String(50), nullable=False, default='SYSTEM')
    rec_crtn_user_id = db.Column(db.String(10), nullable=False, default='GUEST')
    rec_crtn_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    rec_upd_prg_id = db.Column(db.String(50), nullable=False, default='SYSTEM')
    rec_upd_user_id = db.Column(db.String(10), nullable=False, default='GUEST')
    rec_upd_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Contact {self.id}: {self.name}>'
