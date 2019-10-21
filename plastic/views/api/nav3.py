# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint('nav3', __name__, url_prefix='/nav3')


@bp.route('/item1', methods=['GET'])
def gets_item3_1():
    return render_template('detail_problem.html')


@bp.route('/item2', methods=['GET'])
def gets_item3_2():
    return render_template('detail_problem_analyze.html')
