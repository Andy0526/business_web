# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('nav4', __name__, url_prefix='')


@bp.route('/nav4', methods=['GET'])
def gets_nav4():
    return render_template('detail_rank.html')
