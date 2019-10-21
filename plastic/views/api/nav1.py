# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('nav1', __name__, url_prefix='')


@bp.route('/nav1', methods=['GET'])
def gets_nav1():
    return render_template('yqdp.html')
