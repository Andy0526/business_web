# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('support', __name__, url_prefix='')


@bp.route('/support', methods=['GET'])
def gets_nav4():
    return render_template('support.html')
