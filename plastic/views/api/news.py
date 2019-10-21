# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('news', __name__, url_prefix='')


@bp.route('/news', methods=['GET'])
def get_news():
    return render_template('news.html')
