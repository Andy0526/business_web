# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('devices', __name__, url_prefix='')


@bp.route('/devices', methods=['GET'])
def gets_devices():
    return render_template('device.html')

