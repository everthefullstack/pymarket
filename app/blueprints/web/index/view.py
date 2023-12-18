from flask import render_template, redirect, url_for


def index_redirect():
    return redirect(url_for("index_web.index"))

def index():
    return render_template("index.html")


