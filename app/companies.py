from flask import Blueprint, request, redirect, url_for
from flask import render_template


companies = Blueprint("companies", __name__)


@companies.route('/companies')
def companies_page():
    return render_template('companies.html')
