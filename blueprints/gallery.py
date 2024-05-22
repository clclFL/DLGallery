from flask import Blueprint, render_template
from decorators import login_required

bp = Blueprint('gallery', __name__, url_prefix='/gallery')


@bp.route('/pages')
@login_required
def gallery():
    return render_template('gallery.html')
