from decorators.authentication import login_required,admin_required,seller_required
from flask import Blueprint, jsonify, request, render_template, session,url_for,flash
from controllers import home
import controllers.home

home_router = Blueprint('home_router', __name__)


@home_router.route('/add_home',methods=["POST", "GET"])
def add_home():
    if request.method == "POST":
        return controllers.home.add_home()
    return render_template("add_home_for_owner.html")


@home_router.route('/load_home',methods=["POST","GET"])

def load_home():
    return controllers.home.load_home()


@home_router.route('/add_room',methods=["Get","POST"])
def add_room():
    if request.method == "POST":
        return controllers.home.add_room()
    home_id = request.args.get('home_id')
    return render_template("add_room.html",home_id = home_id)

@home_router.route('/info/<int:id>',methods=["GET"])
def info(id):
    return controllers.home.info(id)

