from flask import Blueprint, request, redirect, url_for
from flask import render_template


company_page = Blueprint("company_page", __name__)


@company_page.route('/companies/<company>')
def individual_company_page(company):
    l = ['citi', 'morganstanley']
    if company in l:
        return render_template('company_page.html', data=company)
    else:
        return render_template('not_found.html')