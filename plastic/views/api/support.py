# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('support', __name__, url_prefix='')


@bp.route('/support', methods=['GET'])
@bp.route('/support/<int:id>', methods=['GET'])
def get_support(id=1):
    return render_template('support.html',id=id)
