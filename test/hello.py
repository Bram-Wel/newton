#!/usr/bin/python3
"""Flask test module."""
from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    """Test."""
    return "Index Page"


@app.route("/hello")
def hello_world():
    """Test."""
    return "<p>Hello, World!</p>"


@app.route("/user/<username>")
def user(username):
    """Doc."""
    return f"Username: {escape(username)}"


@app.route("/id/<int:user_id>")
def typer(user_id):
    """Doc."""
    return f"Type: {str(user_id)}"


@app.route("/login", methods=["GET", "POST"])
def login():
    """Doc."""
    if request.method == "POST":
        return "POST method => Perform the login."
    return "GET method => Show login form."


# Alternatively
@app.get("/loader")
def loader_get():
    """Doc."""
    return "Get form"


@app.post("/loader")
def loader_post():
    """Doc."""
    return "Do load."
