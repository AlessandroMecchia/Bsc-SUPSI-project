from flask import Flask
from . import database  # or just import the file to trigger it
from .routes.activities import activities_bp
from .routes.athletes import athletes_bp
from .routes.analytics import analytics_bp

def create_app():
    app = Flask(__name__)

    #  Register blueprints with URL prefixes
    app.register_blueprint(activities_bp, url_prefix="/activities")
    app.register_blueprint(athletes_bp, url_prefix="/athletes")
    app.register_blueprint(analytics_bp, url_prefix="/analytics")

    return app
