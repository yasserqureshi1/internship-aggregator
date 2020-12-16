from flask import Blueprint, request, redirect, url_for
from flask import render_template


home = Blueprint("home", __name__)


@home.route('/')
def base_page():
    return render_template('home.html')

