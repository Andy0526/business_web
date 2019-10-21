# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('nav2', __name__, url_prefix='')


@bp.route('/nav2', methods=['GET'])
def gets_nav2():
    return render_template('info.html')
