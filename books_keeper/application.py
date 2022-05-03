from flask import Flask, flash, redirect, \
            render_template, request, session, url_for

from functools import wraps
from book_manager import BookManager
from user_manager import UserManager

# Configure application
# sess = Session()
app = Flask(__name__)
app.config.from_object(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap


def switch(response):
    exceptions = ("not enough data to add",
                  "no data matches your request", "inserted")
    if response in exceptions:
        flash(response)
        return redirect("/hello")
    else:
        # todo was search, response shall be list
        return render_template("hello.html", data=response, error="")


@app.route("/hello", methods=["GET", "POST"])
@login_required
def hello():

    user_email = "[" + session["email"] + "]"
    bookMan = BookManager(user_email)

    if request.method == "POST":
        # TODO: Add / search entry into the database
        todo, query = get_forms()
        if todo:
            response = bookMan.process_query(todo, query)
            return switch(response)
        else:
            return redirect("/hello")
    else:
        # TODO: Display the entries in the database on index.html
        sel_all = {"author": "", "title": "", "tags": ""}
        data = bookMan.process_regexp_search(sel_all)
        # print(user_email)
        return render_template("hello.html", data=data, error="")


@app.route("/logout")
def logout():
    session["logged_in"] = False
    # session["books"] = False
    session["email"] = False
    flash("you were logged out")
    return redirect(url_for('login'))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        ret = UserManager().register_user(email, password)
        if ret == "success":
            flash("register successfully!")
            return redirect('/login')
        else:
            flash(ret)
            return render_template("register.html", error="")
    else:
        if "logged_in" in session and session["logged_in"]:
            session["logged_in"] = False
        return render_template("register.html", error="")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        # Debug mode "1" - "1"
        if email == "1" and password == "1":
            session["logged_in"] = True
            session["email"] = "books"
            return redirect('/hello')
        else:
            if UserManager().is_log_in(email, password):
                session["logged_in"] = True
                session["email"] = email
                return redirect('/hello')
            else:
                flash("pair login/ password - incorrect!")
                return render_template("login.html", error="")
    else:
        if "logged_in" in session and session["logged_in"]:
            return redirect('/hello')
        return render_template("login.html", error="")


def get_forms():
    clear = request.form.get("show_all")
    print("clear", clear)

    if clear == "Show all table":
        query = {"author": "", "title": "", "tags": ""}
        todo = None
    else:
        author = request.form.get("p-author", type=str)
        title = request.form.get("p-title", type=str)
        tags = request.form.get("p-tags", type=str)
        todo = request.form.get("todo", type=str)
        query = {"author": author.strip(),
                 "title": title.strip(), "tags": tags.strip()}
    return (todo, query)


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.secret_key = 'my secret key'
    # app.config['SESSION_TYPE'] = 'memcache'

    # sess.init_app(app)

    app.run(debug=True)     # , host="0.0.0.0"
