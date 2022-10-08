from flask import Flask

app = Flask(__name__)
# app.config.from_object("config.DevelopmentConfig")

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.form_object("config.DevelopmentConfig")

from app import views
from app import admin_views
from app import error_handles
