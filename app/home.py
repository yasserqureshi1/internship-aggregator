from flask import Blueprint, request, redirect, url_for, flash
from flask import render_template
from app.models import Companies, db


home = Blueprint("home", __name__)


@home.route('/')
def base_page():
    return render_template('home.html')
