# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('info', __name__, url_prefix='')


@bp.route('/info', methods=['GET'])
def gets_nav5():
    return render_template('info.html')
