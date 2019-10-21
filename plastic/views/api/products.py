# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('products', __name__, url_prefix='')


@bp.route('/products', methods=['GET'])
def get_products():
    return render_template('products.html')
