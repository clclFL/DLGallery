from flask import Blueprint, render_template

bp = Blueprint('indexWorkbench', __name__, url_prefix='/')


@bp.route('/')
def index_page():
    return render_template('index.html')
