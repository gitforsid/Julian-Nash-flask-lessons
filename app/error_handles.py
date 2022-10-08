from app import app

from flask import render_template, request


@app.errorhandler(404)
def not_found(e):

    return render_template("/public/404.html")


@app.errorhandler(500)
def not_found(e):
    app.logger.error(f"server error: {e} , route: {request.url}")
    return render_template("/public/500.html")
