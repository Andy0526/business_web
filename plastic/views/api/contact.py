# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('contact', __name__, url_prefix='')


@bp.route('/contact', methods=['GET'])
def get_news():
    return render_template('contact.html')
