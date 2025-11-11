# Hatano-Lab/app/models/article.py
from app import db # Flask-SQLAlchemyのdbインスタンスをインポート
from sqlalchemy.schema import Sequence
from datetime import datetime

# 記事情報を格納するモデル (ATC000 記事情報)
class Article(db.Model):
    # テーブル名
    __tablename__ = 'articles'

    # --- 主キー・基本情報 ---
    # 記事ID (記事ID) - 要件F-i/D-i。主キーとして自動採番(SERIAL)
    id = db.Column('article_id', db.Integer, Sequence('article_id_seq'), primary_key=True)
    
    # 記事画像パス (記事画像パス)
    image_path = db.Column('article_image_path', db.String(255), nullable=True)
    
    # 記事タイトル (記事タイトル) - 要件F-ii/D-ii
    title = db.Column('article_title', db.String(100), nullable=False)
    
    # 記事本文 (記事本文) - 要件F-iv/D-iv
    body = db.Column('article_body', db.Text, nullable=False)
    
    # 記事カテゴリーID (記事カテゴリーID) - 関連情報
    # (Categoryモデルが存在しないため、ここではIntegerで定義)
    category_id = db.Column('article_category_id', db.Integer, nullable=True) 
    
    # --- システム情報・制御フラグ ---
    # 削除フラグ (削除フラグ) - 要件D-IIにより必須
    # 0: 削除OFF (有効), 1: 削除ON (無効)
    deleted_flg = db.Column('deleted_flg', db.SmallInteger, default=0, nullable=False)

    # レコード作成プログラムID (レコード作成プログラムID)
    rec_crtn_prg_id = db.Column('rec_crtn_prg_id', db.String(50), nullable=False, default='SYSTEM')
    
    # レコード作成ユーザID (レコード作成ユーザID)
    rec_crtn_user_id = db.Column('rec_crtn_user_id', db.String(10), nullable=False, default='GUEST')
    
    # レコード作成時刻印 (レコード作成時刻印)
    rec_crtn_tmstmp = db.Column('rec_crtn_tmstmp', db.DateTime, default=datetime.utcnow, nullable=False)
    
    # レコード更新プログラムID (レコード更新プログラムID)
    rec_upd_prg_id = db.Column('rec_upd_prg_id', db.String(50), nullable=False, default='SYSTEM')
    
    # レコード更新ユーザID (レコード更新ユーザID)
    rec_upd_user_id = db.Column('rec_upd_user_id', db.String(10), nullable=False, default='GUEST')
    
    # レコード更新時刻印 (レコード更新時刻印)
    # レコードが更新されるたびに自動で更新
    rec_upd_tmstmp = db.Column('rec_upd_tmstmp', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Article {self.id}: {self.title}>'