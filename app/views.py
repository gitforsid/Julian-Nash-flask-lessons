from app import app

from flask import render_template, request, redirect, jsonify, make_response, url_for
from flask import send_from_directory, abort, session, flash


from datetime import datetime

import os

from werkzeug.utils import secure_filename


@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")


@app.route("/")
def index():
    # print(app.config)
    # app.config["SECRET_KEY"] = "djjdjdjdjjd"
    # print(app.config["SECRET_KEY"])
    
    # abort(500)

    # print(app.config["ENV"])
    return render_template("public/index.html")


@app.route("/public_templates")
def public_templates():
    return render_template("public/templates/public_templates.html")


@app.route("/jinja")
def jinja():
    my_name = "Bohdan"

    age = 30

    langs = ["python", "JavaScript", "PHP"]

    friends = {
    "tom":30,
    "sem":11,
    "Julian":40,
    "tony":20
    }

    cool = True

    colors = ("red", "blue", "green")

    class GitRemote(object):
        def __init__(self, name, description, url):
            self.name = name
            self.description = description
            self.url = url

        def pull(self):
            return f"pulling repo {self.name}"

        def clon(self):
            return f"Cloning into {self.url}"

    my_remote = GitRemote(
        name="Flask jinja",
        description="Template design tutorial",
        url="https://www.youtube.com"
    )

    def repeat(x, qty):
        return x * qty

    date = datetime.utcnow()

    my_html = "<h3> huj</h3>"

    return render_template("public/jinja.html", my_name=my_name, age=age, langs=langs,
    friends=friends, cool=cool, colors=colors, GitRemote=GitRemote, repeat=repeat, my_remote=my_remote,
    date=date, my_html=my_html
     )


@app.route("/about")
def about():
    return render_template("public/about.html")


@app.route("/sing_up1", methods = ['POST', 'GET'])
def sing_up1():

    if request.method == 'POST':

        req = request.form

        username = req["username"]
        email = req.get("email")
        password = request.form["password"]

        print(username, email, password)

        return redirect(request.url)

    return render_template("public/sing_up1.html")


users = {
    "mitsuko":{
    "name": "Amir Nor",
    "bio": "programmer of some lenguage ",
    "twitter": "@gitfor"
    },
    "suko":{
    "name": " Nor",
    "bio": "programmer of some esej ",
    "twitter": "@gfor"
    },
    "suo":{
    "name": " Noriii",
    "bio": "programmer of some poem ",
    "twitter": "@gfodddddr"
    }
}


@app.route("/dinemic/<username>")
def dinemic(username):

    user = None

    if username in users:
        user = users[username]

    return render_template("public/dinemic.html", user=user, username=username)


@app.route("/multiple/<foo>/<bar>/<baz>")
def multiple(foo, bar, baz):
    return f"foo is {foo}, bar is {bar}, baz is {baz}"


@app.route("/json", methods=["POST"])
def json():
    if request.is_json:
        req = request.get_json()
        response = {
            "message": "JSON recived",
            "name": req.get("neme")
        }

        res = make_response(jsonify(response), 200)
        return res
    else:
        res = make_response(jsonify({"message": "no json recived"}), 400)
        return res


    # req = request.get_json()
    # print(type(req))
    # print(req)
    # return "Thanks", 200


@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")


@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    #res = make_response(jsonify({ "massage": "some massage"}), 200)
    res = make_response(jsonify(req), 200)
    return res


@app.route("/query")
def query():
    # args = request.args

    # for k, v in args.items():
    #     print(f"{k}: {v}")

    # if "foo" in args:
    #     foo = args.get("foo")
    # print(foo)

    # if request.args:
    #     args = request.args
    #     if "title" in args:
    #         title = request.args.get("title")
    #     print(title)

    # print(request.query_string)

    if request.args:
        args = request.args
        serialized = ",".join(f"{k}:{v}" for k, v in args.items())

        return f"(Query) {serialized}", 200

    else:

        return "No Query arguments", 200


app.config["IMAGE_UPLOADS"] = "/Users/bogdangulencin/PycharmProjects/just_one_more_night /app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENTINS"] = ['PNG', 'JPEG', 'JPG', 'GIF']
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024


def alloved_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENTINS"]:
        return True
    else:
        return False


def alloved_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route("/upload_image", methods=["POST", "GET"])
def upload_image():
    if request.method == "POST":
        if request.files:
            if not alloved_image_filesize(request.cookies.get("filesize")):
                print("file exceeded maximum size")
                return redirect(request.url)
            # print(request.cookies)
            image = request.files["image"]

            if image.filename == "":
                print("image must have a name")
                return redirect(request.url)

            if not alloved_image(image.filename):
                print("this image extention is not alloved")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

            print("image is saved")
            return redirect(request.url)
    return render_template("public/upload_image.html")


app.config["CLIENT_IMAGEN"] = "/Users/bogdangulencin/PycharmProjects/just_one_more_night /app/static/client/img"
app.config["CLIENT_CSV"] = "/Users/bogdangulencin/PycharmProjects/just_one_more_night /app/static/client/csv"


@app.route("/get_image/<image_name>")
def get_image(image_name):

    try:
        return send_from_directory(app.config["CLIENT_IMAGEN"], path=image_name, as_attachment=False)
    except FileNotFoundError:
        abort(404)


@app.route("/get_csv/<filename>")
def get_csv(filename):

    try:
        return send_from_directory(app.config["CLIENT_CSV"], path=filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)


#для структури в тезі route удобно виуористувати @app.route("/get_report/<path:path>")


@app.route("/cookies")
def cookies():
    res = make_response("cookies", 200)
    cookies = request.cookies

    flavor = cookies.get("flavor")
    chop_type = cookies.get("chocolate chip")
    chewy = cookies.get("chewy")

    print(flavor)

    res.set_cookie(
        "flavor",
        value="chocolate chip",
        max_age=10,
        expires=None,
        path=request.path,
        domain=None,
        secure=False,
        httponly=False,
        samesite=None,
    )

    res.set_cookie("chocolate chip", "dark")
    res.set_cookie("chewy", "yes")
    return res


app.config["SECRET_KEY"] = "djdjdjdj"


userID = {
    "julian":{
    "username": "julian",
    "email": "julian@gmail.com",
    "password": "someexampl",
    "bio": "some programmer from sa"
    },
    "clarisa":{
    "username": "clarisa",
    "email": "clarisa@gmail.com",
    "password": "",
    "bio": "some programmer from la"
    },
}


@app.route("/sing_in", methods=["GET", "POST"])
def sing_in():
    if request.method == "POST":
        req = request.form
        username = req.get("username")
        password = req.get("password")
        print(username, password)

        if not username in userID:
            print("username not found")
            return redirect(request.url)
        else:
            user = userID[username]

        if not password == user["password"]:
            print("password incorrect")
            return redirect(request.url)

        else:
            session["USERNAME"] = user["username"]
            print("user added to session")
            return redirect(url_for("profile"))

    return render_template("public/sing_in.html")


@app.route("/profile")
def profile():
    if session.get("USERNAME", None) is not None:
        username = session.get("USERNAME")
        user = userID[username]
        return render_template("/public/profile.html", user=user)
    else:
        print("username not found in session")
        return redirect(url_for("sing_in"))


@app.route("/sign_out")
def sign_out():
    session.pop("USERNAME", None)
    return redirect(url_for("sing_in"))


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        req = request.form

        username = req.get("username")
        email = req.get("email")
        password = req.get("password")

        if not len(password) >= 10:
            flash("passwors mast be least 10 charakters in lengt", "warning")
            return redirect(request.url)

        flash("account created", "danger")
        return redirect(request.url)

    return render_template("public/sign_up.html")


@app.route("/bb")
def bb():
    return render_template("/public/bb.html")
