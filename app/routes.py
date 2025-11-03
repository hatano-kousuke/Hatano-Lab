# app/routes.py
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # 必要なら将来的にDBやモデルからデータを渡す
    return render_template('index.html')
