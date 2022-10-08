from app import app

from flask import render_template


@app.route("/admin_base")
def admin_base():
    return render_template("admin/template/admin_templates.html")


@app.route("/aboutss")
def som_for_admin():
    return render_template("admin/about_admin.html")
