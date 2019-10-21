# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('nav5', __name__, url_prefix='')


@bp.route('/nav5', methods=['GET'])
def gets_nav5():
    return render_template('detail_navigation.html')
