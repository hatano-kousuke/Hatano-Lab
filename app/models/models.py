from sqlalchemy import Column, String, TIMESTAMP
from flask_login import UserMixin
from .base import Base

class User(Base, UserMixin):
    __tablename__ = 'USR000'  # テーブル名を指定（ユーザ情報）

    # ユーザID（主キー）
    usr_id = Column(String(10), primary_key=True, nullable=False, comment="ユーザを一意に表すID")

    # パスワード
    usr_pw = Column(String(16), nullable=False, comment="ユーザのログインパスワード")

    # 削除フラグ（0:未削除, 1:削除済）
    delt_flg = Column(String(1), nullable=False, comment="レコードの削除状態を示すフラグ")

    # 作成プログラムID
    rec_crtn_prg_id = Column(String(50), comment="レコードを作成したプログラムのID")

    # 作成ユーザID
    rec_crtn_usr_id = Column(String(10), comment="レコードを作成したユーザのID")

    # 作成日時
    rec_crtn_tmstmp = Column(TIMESTAMP, comment="レコード作成日時")

    # 更新プログラムID
    rec_upd_prg_id = Column(String(50), comment="レコードを更新したプログラムのID")

    # 更新ユーザID
    rec_upd_usr_id = Column(String(10), comment="レコードを更新したユーザのID")

    # 更新日時
    rec_upd_tmstmp = Column(TIMESTAMP, comment="レコード更新日時")
