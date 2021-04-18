from flask import Blueprint, request, redirect, url_for, flash
from flask import render_template, abort
from app.models import Companies, Positions, db


views = Blueprint("views", __name__)


@views.route('/', methods=['GET', 'POST'])
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
    

    return render_template('index.html', new_pos=new_pos, close_pos=close_pos, browse=browse)


@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        s = request.form['search']
        if s != '':
            query = Positions.query.filter(Positions.name.like('%' + s + '%')).all()
        else:
            query = Positions.query.order_by(Positions.name).limit(10).all()
    else:
        query = Positions.query.order_by(Positions.name).limit(10).all()
    
    results = []
    for item in query:
        company = Companies.query.filter_by(id=item.company_id).first()
        results.append({
            'company': company.name,
            'name': item.name,
            'url': item.url,
            'location': item.location,
            'description': item.description,
            'lastupdated': item.date_posted,
            'job_type': item.job_type
        })
    return render_template('search.html', results=results)


@views.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@views.route('/list-of-companies', methods=['GET', 'POST'])
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
    
        if 'search' in request.form:
            s = request.form['search']
            query = Companies.query.filter(Companies.name.like('%' + s + '%')).order_by(Companies.name).all()
            search = []
            for q in query:
                no_open = Positions.query.filter_by(company_id=q.id).all()
                search.append({'name': q.name, 'industry': q.industry, 'no-open': len(no_open), 'description':q.description, 'link': f'companies/{q.url}'})
    
    else:
        query = Companies.query.filter(Companies.name.startswith('A')).order_by(Companies.name).all()
        search = []
        for q in query:
            open_pos = Positions.query.filter_by(company_id=q.id).all().count()
            search.append({'name': q.name, 'industry': q.industry, 'no-open': open_pos, 'description':q.description})
    return render_template('companies.html', search=search)


@views.route('/companies/<company>', methods=['GET'])
def ind_company(company):
    query = Companies.query.filter_by(url=company).first()
    if query is None:
        abort(404)
    else:
        details = {'name': query.name, 'description': query.description}
        pos = Positions.query.filter_by(company_id=query.id).all()

        return render_template('company.html', details=details, browse=pos)

