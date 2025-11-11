import logging
from logging.config import fileConfig
from flask import current_app
from alembic import context

# Alembic 設定オブジェクト
config = context.config

# ログ設定
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# ======================================================
# ここからアプリケーションのモデルを読み込む設定部分
# ======================================================

# Flask-SQLAlchemy の db をインポート
from app import db

# Base を継承するモデル群（USR000 / USR001）
from app.models.base import Base
from app.models.user import User, Password

# db.Model を継承するモデル群（Article / Contact など）
from app.models.article import Article
from app.models.contact import Contact, ContactCategory

# --- 両方の metadata を Alembic に認識させる ---
target_metadata = [db.metadata, Base.metadata]

# ======================================================
# データベース接続設定部分
# ======================================================

def get_engine():
    """Flask-SQLAlchemy 3.x / 2.x 両対応"""
    try:
        # Flask-SQLAlchemy < 3.x 用
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # Flask-SQLAlchemy >= 3.x 用
        return current_app.extensions['migrate'].db.engine

def get_engine_url():
    """接続URLを取得"""
    try:
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')

config.set_main_option('sqlalchemy.url', get_engine_url())

# ======================================================
# マイグレーション実行関数群
# ======================================================

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode'."""

    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args
        )

        with context.begin_transaction():
            context.run_migrations()


# ======================================================
# 実行モード切替
# ======================================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
