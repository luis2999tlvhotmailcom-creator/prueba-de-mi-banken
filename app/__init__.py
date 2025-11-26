from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.settings import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ CONFIGURACIÓN CORS MÁS AGRESIVA
    CORS(app, 
         resources={r"/*": {"origins": "*"}},
         supports_credentials=True,
         allow_headers=["*"],
         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    
    # ✅ DESHABILITAR REDIRECCIÓN PARA OPTIONS
    @app.before_request
    def handle_options():
        from flask import request
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
            for key, value in headers.items():
                response.headers[key] = value
            return response

    db.init_app(app)
    migrate.init_app(app, db)

    # Importación de rutas
    from app.routes.medications_routes import medication_bp
    from app.routes.patients_routes import patient_bp
    from app.routes.deliveries_routes import delivery_bp
    from app.routes.suppliers_routes import supplier_bp
    from app.routes.purchases_routes import purchase_bp
    from app.routes.purchase_detail_routes import purchase_detail_bp

    # Registro de blueprints
    app.register_blueprint(medication_bp, url_prefix="/medications")
    app.register_blueprint(patient_bp, url_prefix="/patients")
    app.register_blueprint(delivery_bp, url_prefix="/deliveries")
    app.register_blueprint(supplier_bp, url_prefix="/suppliers")
    app.register_blueprint(purchase_bp, url_prefix="/purchases")
    app.register_blueprint(purchase_detail_bp, url_prefix="/purchase-details")

    return app
