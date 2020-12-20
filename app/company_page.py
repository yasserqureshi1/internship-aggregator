from flask import Blueprint, abort
from flask import render_template
from app.models import Companies, Positions

company_page = Blueprint("company_page", __name__)


@company_page.route('/companies/<company>')
def individual_company_page(company):
    comp = Companies.query.filter_by(url=company).first()
    if comp is not None:
        pos = Positions.query.filter_by(company_id=comp.id)
        return render_template('company_page.html', company=comp, positions=pos)
    else:
        abort(404)
