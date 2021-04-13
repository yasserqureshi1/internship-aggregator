from flask import Blueprint, request, redirect, url_for, flash
from flask import render_template, abort
from app.models import Companies, Positions, db


index = Blueprint("index", __name__)


@index.route('/', methods=['GET', 'POST'])
def base_page():
    # New Positions
    query = Positions.query.order_by(Positions.date_posted).limit(10).all()
    new_pos = []
    for pos in query:
        new_pos.append(
            {'company': Companies.query.filter_by(id=pos.company_id).first().name, 'title': pos.name, 'location':pos.location, 'description':pos.description, 'lastupdated': pos.date_posted, 'job_type':pos.job_type, 'url':pos.url},
        )

    # Closing Positions
    query = Positions.query.order_by(Positions.date_closing).limit(10).all()
    close_pos = []
    for pos in query:
        close_pos.append(
            {'company': Companies.query.filter_by(id=pos.company_id).first().name, 'title': pos.name, 'location':pos.location, 'description':pos.description, 'lastupdated': pos.date_posted, 'job_type':pos.job_type, 'url':pos.url},
        )

    # Browse
    query = Positions.query.limit(10).all()
    browse = []
    for pos in query:
        browse.append(
            {'company': Companies.query.filter_by(id=pos.company_id).first().name, 'title': pos.name, 'location':pos.location, 'description':pos.description, 'lastupdated': pos.date_posted, 'job_type':pos.job_type, 'url':pos.url},
        )
    return render_template('new/index.html', new_pos=new_pos, close_pos=close_pos, browse=browse)


@index.route('/about', methods=['GET'])
def about():
    return render_template('new/about.html')


@index.route('/list-of-companies', methods=['GET', 'POST'])
def list_of_companies():
    if request.method == 'POST':
        if 'alpha' in request.form:
            query = Companies.query.filter(Companies.name.startswith(request.form['alpha'].upper())).order_by(Companies.name).all()
            if query is None:
                search = {}
            else:
                search = []
                for q in query:
                    no_open = Positions.query.filter_by(company_id=q.id).all()
                    search.append({'name': q.name, 'industry': q.industry, 'no-open': len(no_open), 'description':q.description, 'link': f'companies/{q.url}'})
    else:
        query = Companies.query.filter(Companies.name.startswith('A')).order_by(Companies.name).all()
        search = []
        for q in query:
            open = Positions.query.filter_by(company_id=q.id).all().count()
            search.append({'name': q.name, 'industry': q.industry, 'no-open': open, 'description':q.description})
    return render_template('new/companies.html', search=search)


@index.route('/companies/<company>', methods=['GET'])
def ind_company(company):
    query = Companies.query.filter_by(url=company).first()
    if query is None:
        abort(404)
    else:
        details = {'name': query.name, 'description': query.description}
        pos = Positions.query.filter_by(company_id=query.id).all()

        return render_template('new/company.html', details=details, browse=pos)
