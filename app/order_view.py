

from flask import Blueprint, render_template, session

house_blueprint = Blueprint('order', __name__)


@house_blueprint.route('/booking/', methods=['GET'])
def myhouse():
    return render_template('myhouse.html')