from flask import Blueprint, request, redirect, url_for, flash
from flask import render_template
from app.models import Companies, db


index = Blueprint("index", __name__)


@index.route('/', methods=['GET', 'POST'])
def base_page():
    new_pos = [{'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'},
    {'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'},
    {'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'},
    {'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'},
    {'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'},
    {'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'},
    {'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'},
    {'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'},
    {'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'},
    {'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'},
    {'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'},
    {'company': 'Apple', 'title': 'Software dev', 'location':'UK', 'description':'A great job', 'lastupdated': '12/09/2020', 'job_type':'Internship', 'url':'https://www.google.com'}]
    if request.method == 'POST':
        # Alphabet search
        if 'alpha' in request.form:
            print(request.form['alpha'])
    

    return render_template('new/companies.html')
    #return render_template('home.html')


@index.route('/about', methods=['GET'])
def about():
    return 


@index.route('/list-of-companies', methods=['GET', 'POST'])
def list_of_companies():
    return


@index.route('/companies/<company>', methods=['GET'])
def ind_company(company):
    return
