# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('products', __name__, url_prefix='')


@bp.route('/products/<int:item_id>', methods=['GET'])
def get_products(item_id=0):
    return render_template('products.html')
