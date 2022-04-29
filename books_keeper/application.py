from flask import Flask, redirect, \
            render_template, request
# , session, flash, jsonify
# from flask.ext.session import Session
from db_manager import SqlManager
from process_manager import ProcessManager

# Configure application
# sess = Session()
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


def get_forms():
    clear = request.form.get("show_all")
    print("clear", clear)

    if clear == "Show all table":
        query = {"author": "", "name": "", "tags": ""}
        todo = None
    else:
        author = request.form.get("p-author", type=str)
        name = request.form.get("p-name", type=str)
        tags = request.form.get("p-tags", type=str)
        todo = request.form.get("todo", type=str)
        query = {"author": author.strip(),
                 "name": name.strip(), "tags": tags.strip()}
    return (todo, query)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        # TODO: Add the user's entry into the database
        todo, query = get_forms()
        if todo:
            ret = ProcessManager.process_query(todo, query)

            if ret == "not_enough_to_add":
                error = "not enough data to add"
                return render_template("index.html", data=[], error=error)
            elif ret == []:
                error = "no data matches your request"
                return render_template("index.html", data=[], error=error)
            elif ret == "inserted":
                return redirect("/")
            else:
                return render_template("index.html", data=ret, error="")
        else:
            return redirect("/")
    else:
        # TODO: Display the entries in the database on index.html
        data = SqlManager().select_sql()
        # print(data)
        return render_template("index.html", data=data, error="")


if __name__ == "__main__":
    app.secret_key = 'my secret key'
    app.config['SESSION_TYPE'] = 'memcache'

    # sess.init_app(app)

    app.run()
