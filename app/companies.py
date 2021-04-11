from flask import Blueprint
from flask import render_template
from app.models import Companies, Positions


companies = Blueprint("companies", __name__)


@companies.route('/companies')
def companies_page():
    all = Companies.query.all()
    return render_template('companies.html', list_of_companies=all)


@companies.route('/companies/<company>')
def individual_company_page(company):
    comp = Companies.query.filter_by(url=company).first()
    if comp is not None:
        pos = Positions.query.filter_by(company_id=comp.id)
        return render_template('company_page.html', company=comp, positions=pos)
    else:
        abort(404)