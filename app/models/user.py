# Hatano-Lab/app/models/user.py
from sqlalchemy import Column, String, Date, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from .base import Base

class User(Base, UserMixin):
    """
    USR000 ユーザ情報
    """
    __tablename__ = 'USR000'

    # ユーザID（主キー）
    usr_id = Column(String(10), primary_key=True, nullable=False, comment="ユーザを一意に表すID")

    # ユーザ氏名
    usr_nm = Column(String(50), nullable=False, comment="ユーザ氏名")

    # ユーザ利用開始日
    usr_strt_date = Column(Date, nullable=False, comment="ユーザ利用開始日")

    # ユーザ利用終了日
    usr_end_date = Column(Date, nullable=True, comment="ユーザ利用終了日")

    # 削除フラグ（0:未削除, 1:削除済）
    delt_flg = Column(String(1), nullable=False, default="0", comment="レコード削除フラグ")

    # レコード作成情報
    rec_crtn_prg_id = Column(String(50), comment="レコード作成プログラムID")
    rec_crtn_usr_id = Column(String(10), comment="レコード作成ユーザID")
    rec_crtn_tmstmp = Column(TIMESTAMP, comment="レコード作成時刻印")

    # レコード更新情報
    rec_upd_prg_id = Column(String(50), comment="レコード更新プログラムID")
    rec_upd_usr_id = Column(String(10), comment="レコード更新ユーザID")
    rec_upd_tmstmp = Column(TIMESTAMP, comment="レコード更新時刻印")

    # リレーション：パスワード情報（USR001）を紐付け
    password_info = relationship("Password", back_populates="user", uselist=False)

class Password(Base):
    """
    USR001 パスワード情報
    """
    __tablename__ = 'USR001'

    # ユーザID（USR000 への外部キー）
    usr_id = Column(String(10), ForeignKey("USR000.usr_id"), primary_key=True, nullable=False, comment="ユーザID")

    # パスワード
    password = Column(String(255), nullable=False, comment="ユーザのログインパスワード（ハッシュ値）")

    # パスワード更新日時
    pw_upd_tmstmp = Column(TIMESTAMP, comment="パスワード更新日時")

    # 削除フラグ
    delt_flg = Column(String(1), nullable=False, default="0", comment="レコード削除フラグ")

    # レコード作成情報
    rec_crtn_prg_id = Column(String(50), comment="レコード作成プログラムID")
    rec_crtn_usr_id = Column(String(10), comment="レコード作成ユーザID")
    rec_crtn_tmstmp = Column(TIMESTAMP, comment="レコード作成時刻印")

    # レコード更新情報
    rec_upd_prg_id = Column(String(50), comment="レコード更新プログラムID")
    rec_upd_usr_id = Column(String(10), comment="レコード更新ユーザID")
    rec_upd_tmstmp = Column(TIMESTAMP, comment="レコード更新時刻印")

    # リレーション：USR000との紐付け
    user = relationship("User", back_populates="password_info")
