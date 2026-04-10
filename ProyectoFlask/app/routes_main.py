from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/platos_page")
def platos_page():
    return render_template("platos.html")

@main_bp.route("/pedido_page")
def pedido_page():
    return render_template("pedido.html")

@main_bp.route("/menu_page")
def menu_page():
    return render_template("menu.html")
@main_bp.route("/add_plato_page")
def add_plato_page():
    return render_template("añadir_plato.html")