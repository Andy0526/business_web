# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('devices', __name__, url_prefix='/devices')


@bp.route('/item1', methods=['GET'])
def gets_item3_1():
    return render_template('device_item1.html')


@bp.route('/item2', methods=['GET'])
def gets_item3_2():
    return render_template('device_item2.html')
