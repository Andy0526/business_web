# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('info', __name__, url_prefix='/info')


@bp.route('/culture', methods=['GET'])
def get_culture():
    return render_template('info_culture.html')


@bp.route('/work', methods=['GET'])
def get_work():
    return render_template('info_work.html')
