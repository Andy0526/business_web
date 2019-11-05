# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('products', __name__, url_prefix='')

@bp.route('/products', methods=['GET'])
@bp.route('/products/<int:item_id>', methods=['GET'])
def get_products(item_id=1):
    return render_template('products.html',item_id=item_id)
