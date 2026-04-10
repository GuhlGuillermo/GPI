import os
from flask import Flask

def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static")
    )

    from .routes_main import main_bp
    from .routes_platos import platos_bp
    from .routes_menus import menus_bp
    from .routes_pedidos import pedidos_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(platos_bp)
    app.register_blueprint(menus_bp)
    app.register_blueprint(pedidos_bp)

    return app