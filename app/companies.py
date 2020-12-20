from flask import Blueprint
from flask import render_template
from app.models import Companies


companies = Blueprint("companies", __name__)


@companies.route('/companies')
def companies_page():
    all = Companies.query.all()
    return render_template('companies.html', list_of_companies=all)
