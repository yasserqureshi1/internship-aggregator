import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from app.models import Companies, Positions, db
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType
from fp.fp import FreeProxy

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)

proxyObject = FreeProxy(country_id=['GB'], rand=True)


def company_checker(name, description, industry, url):
    """
    This checks whether the company profile is in the db (creates it if not) and deletes all position entries in that company.
    """
    exists = Companies.query.filter_by(name=name).first()  # Checks if company exists in db
    if not exists:  # Adds to db
        comp = Companies(name=name, description=description, industry=industry, url=url)
        db.session.add(comp)
        db.session.commit()
    comp = Companies.query.filter_by(name=name).first()

    pos = Positions.query.filter_by(
        company_id=comp.id).all()  # Deletes all entries for particular company (Prepping for new entries)
    for i in pos:
        db.session.delete(i)
        db.session.commit()
    return comp


def insert_new_positions(name, description, role, location, job_type, date_posted, date_closing, company_id, url):
    """
    Inserts new company positions into db
    """
    pos = Positions.query.filter_by(name=name, company_id=company_id).first()
    if not pos:
        new_pos = Positions(name=name,
                            description=description,
                            role=role,
                            location=location,
                            job_type=job_type,
                            date_posted=date_posted,
                            date_closing=date_closing,
                            company_id=company_id,
                            url=url)
        db.session.add(new_pos)
        db.session.commit()


def check_job(text):
    text = text.lower()
    if 'summer' in text:
        return 'Summer Internship'
    elif '12' or 'placement' or 'year' in text:
        return 'Placement'
    elif 'graduate' or 'full time' in text:
        return 'Graduate'
    return 'NA'


class Scraper:
    def __init__(self):
        #self.BailleGifford() Currently none open
        try:
            self.Citi()
        except Exception as e:
            print(e)
        try:
            self.MorganStanley()
        except Exception as e:
            print(e)
        try:
            self.JPMorgan()
        except Exception as e:
            print(e)
        try:
            self.GoldmanSachs()
        except Exception as e:
            print(e)
        #self.Nomura()
        #self.Royal_Bank_of_Canada()
        #self.UBS()

    def BailleGifford(self):
        print('Getting new listings from Baille Gifford...')
        comp = company_checker(name='Baille Gifford', description='Another company', industry='', url='baille-gifford')

        headers = {
            'User-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'X-Workday-Client': '2020.35.027',
            'Host': 'bailliegifford.wd3.myworkdayjobs.com',
            'Accept': 'application/json,application/xml',
            'workday-client-manifest-id': 'mvp',
            'Referer': 'https://bailliegifford.wd3.myworkdayjobs.com/BaillieGiffordEarlyCareers'}

        url = "https://bailliegifford.wd3.myworkdayjobs.com/BaillieGiffordEarlyCareers"

        html = requests.get(url=url, headers=headers)
        output = json.loads(html.text)
        try:
            for i in output['body']['children'][0]['children'][0]['listItems']:
                insert_new_positions(name=i['title']['instances'][0]['text'],
                                     description='',
                                     role='NA',
                                     location=i['subtitles'][1]['instances'][0]['text'],
                                     job_type='NA',
                                    # date_posted='',
                                     #date_closing='',
                                     company_id=comp.id,
                                     url='NA')
        except:
            print('No Roles')
        print('Baille Gifford Complete')

    def Citi(self):
        print('Getting new listings from Citi Bank...')
        comp = company_checker(name='Citi', description='Another company', industry='', url='citi')

        headers = {'Host': 'jobs.citi.com',
                   'Referer': 'https://jobs.citi.com/search-jobs',
                   'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                                 'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                   'X-Requested-With': 'XMLHttpRequest'}

        data = {'ActiveFacetID': 'Recent+Graduates'}

        url = 'https://jobs.citi.com/search-jobs/results?ActiveFacetID=Recent+Graduates&CurrentPage=1&RecordsPerPage=500&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=Recent+Graduates&FacetFilters%5B0%5D.FacetType=5&FacetFilters%5B0%5D.Count=205&FacetFilters%5B0%5D.Display=Recent+Graduates&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=custom_fields.ECAMPUS&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='

        html = requests.get(url=url, headers=headers, proxies={"http": f"http://{proxyObject.get()}"}, timeout=3)
        output = json.loads(html.text)
        soup = BeautifulSoup(output['results'], 'html.parser')

        job_list = soup.select('a[data-job-id*=""]')
        for i in job_list:
            split = [j for j in i.text.split('\n') if j != '']
            title = split[0]
            location = split[1]
            job_type = 'Internship' if 'summer' in title.lower() else 'Graduate'
            insert_new_positions(name=title,
                                 description='NA',
                                 role='NA',
                                 location=location,
                                 job_type=job_type,
                                 date_posted=datetime.utcnow(),
                                 date_closing=None,
                                 company_id=comp.id,
                                 url='https://jobs.citi.com' + i['href'])

    def GoldmanSachs(self):
        print('Getting new listings from Goldman Sachs...')
        comp = company_checker(name='Goldman Sachs', description='Description to be filled', industry='', url='goldman-sachs')

        url = 'https://www.goldmansachs.com/careers/students/programs/programs-list.json'

        html = requests.get(url=url, headers={'User-Agent': user_agent_rotator.get_random_user_agent()}, proxies={"http": f"http://{proxyObject.get()}"}, timeout=3)
        output = json.loads(html.text)

        for i in output['programs']:

            insert_new_positions(name=i['title'],
                                 description=i['programTypeDescription'],
                                 role='NA',
                                 location=i['region']['name'],
                                 job_type=check_job(i['title']),
                                 date_posted=datetime.utcnow(),
                                 date_closing=None,
                                 company_id=comp.id,
                                 url=f'https://www.goldmansachs.com{i["url"]}')
        print('Goldman Sachs Complete')

    def JPMorgan(self):
        print('Getting new listings from JP Morgan...')
        comp = company_checker(name='J.P. Morgan', description='Description to be filled', industry='',url='jp-morgan')

        url = 'https://careers.jpmorgan.com/services/json/careers/gate/programs.json'

        html = requests.get(url=url, headers={'User-Agent': user_agent_rotator.get_random_user_agent()}, proxies={"http": f"http://{proxyObject.get()}"}, timeout=3)
        output = json.loads(html.text)

        for i in output:
            for j in output[i]:
                days = datetime.fromisoformat(j['end_date']).date() - datetime.now().date()
                if days.days > 0:
                    insert_new_positions(name=j['name'],
                                        description='NA',
                                        role='NA',
                                        location=j['region'],
                                        job_type=j['level'],
                                        date_posted=datetime.utcnow(),
                                        date_closing=datetime.fromisoformat(j['end_date']).date(),
                                        company_id=comp.id,
                                        url=j['application_url'])
        print('JP Morgan Complete')

    def MorganStanley(self):
        print('Getting new listings from Morgan Stanley...')
        comp = company_checker(name='Morgan Stanley', description='Description to be filled', industry='', url='morgan-stanley')

        url = 'https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-3786f0ce9359/candidate/jobboard/vacancy/1' \
              '/adv/?f_Item_Opportunity_13857_lk=765&f_Item_Opportunity_17058_lk=133794&ftq= '

        html = requests.get(url=url, headers={'User-Agent': user_agent_rotator.get_random_user_agent()}, proxies={"http": f"http://{proxyObject.get()}"}, timeout=3)
        output = BeautifulSoup(html.text, 'html.parser')

        job_list = output.select('tr[class*="search_res details_row"]')
        for i in job_list:
            insert_new_positions(name=i['data-title'],
                                 description='NA',
                                 role='NA',
                                 location=i.find_all('td', {'class': 'comm_list_tbody'})[1].text.replace(' ', '').replace('\n', ''),
                                 job_type='NA',
                                 date_posted=datetime.utcnow(),
                                 date_closing=None,
                                 company_id=comp.id,
                                 url=i.find('a', {'class': 'subject'})['href'])
        print('Morgan Stanley Complete')


    def Nomura(self):
        print('Getting new listings from Nomura...')
        comp = company_checker(name='Nomura', description='Description to be filled', industry='', url='nomura')

        url = 'https://nomuracampus.tal.net/vx/lang-en-GB/mobile-0/appcentre-ext/brand-4/xf-5b60ed84bdc9/candidate' \
              '/jobboard/vacancy/1/adv/?f_Item_Opportunity_84825_lk=765&ftq='

        html = requests.get(url=url, headers={'User-Agent': user_agent_rotator.get_random_user_agent()}, proxies={"http": f"http://{proxyObject.get()}"})
        output = BeautifulSoup(html.text, 'html.parser')

        job_list = output.select('tr[class*="search_res details_row"]')
        for i in job_list:
            insert_new_positions(name=i['data-title'],
                                 description='NA',
                                 role='NA',
                                 location='NA',
                                 job_type='NA',
                                 date_posted=None,
                                 date_closing=None,
                                 company_id=comp.id,
                                 url=i.find('a', {'class': 'subject'})['href'])
        print('Nomura Complete')

    def Royal_Bank_of_Canada(self):
        print('Getting new listings from Royal Bank of Canada...')
        comp = company_checker(name='Royal Bank of Canada', description='Description to be filled', industry='',
                               url='royal-bank-of-canada')

        url = 'https://rbccmgraduates.gtisolutions.co.uk/Search/CandidateVacancies?facet=on&facet.field=%7B!ex' \
              '%3Dfacetstring_VacancyDetail_Role_Text%7Dfacetstring_VacancyDetail_Role_Text&facet.field=%7B!ex' \
              '%3Dfacetstring_VacancyDetail_Programme_Text%7Dfacetstring_VacancyDetail_Programme_Text&facet.field=%7B!ex' \
              '%3Dfacetstring_VacancyDetail_JobLocation_Text%7Dfacetstring_VacancyDetail_JobLocation_Text&facet.field=%7B' \
              '!ex%3Dfacetstring_VacancyDetail_IntakeYear_Text%7Dfacetstring_VacancyDetail_IntakeYear_Text&facet.limit=-1' \
              '&facet.mincount=1&facet.query=%7B!ex%3Ddynamicdate_VacancyPosting_ScheduledCloseDate+key%3D' \
              '%22dynamicdate_VacancyPosting_ScheduledCloseDate%7C%7CToday%22' \
              '%7Ddynamicdate_VacancyPosting_ScheduledCloseDate:%5BNOW%2FDAY+TO+NOW%2FDAY%5D&facet.query=%7B!ex' \
              '%3Ddynamicdate_VacancyPosting_ScheduledCloseDate+key%3D%22dynamicdate_VacancyPosting_ScheduledCloseDate%7C' \
              '%7CIn+the+next+24+hours%22%7Ddynamicdate_VacancyPosting_ScheduledCloseDate:%5BNOW%2FDAY+TO+NOW%2FDAY' \
              '%2B1DAY%5D&facet.query=%7B!ex%3Ddynamicdate_VacancyPosting_ScheduledCloseDate+key%3D' \
              '%22dynamicdate_VacancyPosting_ScheduledCloseDate%7C%7CWithin+the+next+3+days%22' \
              '%7Ddynamicdate_VacancyPosting_ScheduledCloseDate:%5BNOW%2FDAY+TO+NOW%2FDAY%2B3DAY%5D&facet.query=%7B!ex' \
              '%3Ddynamicdate_VacancyPosting_ScheduledCloseDate+key%3D%22dynamicdate_VacancyPosting_ScheduledCloseDate%7C' \
              '%7CWithin+the+next+week%22%7Ddynamicdate_VacancyPosting_ScheduledCloseDate:%5BNOW%2FDAY+TO+NOW%2FDAY' \
              '%2B7DAY%5D&fl=dbid&fl=dynamicstring_Vacancy_SearchId&fl=title&fl' \
              '=dynamicstring_VacancyDetail_Description_Text&fl=dynamicstring_Vacancy_PostingStatus&fl' \
              '=dynamicmultistrings_Details&fl=dynamicstring_ShortName&json.nl=map&q=*:*&rows=100&sort' \
              '=facetstring_Vacancy_Name+asc&start=0&ts=1599319232462&wt=json'

        html = requests.get(url)
        output = json.loads(html.text)

        for i in output['response']['docs']:
            insert_new_positions(name=i['title'],
                                 description='',
                                 role='NA',
                                 location='NA',
                                 job_type='NA',
                                 date_posted=None,
                                 date_closing=None,
                                 company_id=comp.id,
                                 url=f'https://rbccmgraduates.gtisolutions.co.uk/{i["dynamicstring_ShortName"]}/{i["dbid"]}/viewdetails')
        print('Royal Bank of Canada Complete')

    def UBS(self):
        print('Getting new listings from UBS...')
        comp = company_checker(name='UBS', description='Description to be filled', industry='', url='ubs')

        url = 'https://jobs.ubs.com/TGnewUI/Search/Home/HomeWithPreLoad?partnerid=25008&siteid=5131&PageType' \
              '=searchResults&SearchType=linkquery&LinkID=3858#keyWordSearch=&locationSearch= '

        html = requests.get(url)
        output = BeautifulSoup(html.text, 'html.parser')

        for i in output['searchResultsResponse']['Jobs']['Job']:
            for j in i['Questions']:
                if j['QuestionName'] == 'jobtitle':
                    print(j['Value'])
                elif j['QuestionName'] == 'formtext23':
                    print(j['Value'])
                elif j['QuestionName'] == 'formtext21':
                    print(j['Value'])
                elif j['QuestionName'] == 'lastupdated':
                    print(j['Value'])
                elif j['QuestionName'] == 'reqid':
                    reqid = j['Value']
                elif j['QuestionName'] == 'clientid':
                    clientid = j['Value']
                elif j['QuestionName'] == 'siteid':
                    siteid = j['Value']
            print('https://jobs.ubs.com/TGnewUI/Search/home/HomeWithPreLoad?partnerid=' + str(
                clientid) + '&siteid=' + str(
                siteid) + '&PageType=JobDetails&jobid=' + str(reqid))
            print(' ')

            insert_new_positions(name=i['data-title'],
                                 description='',
                                 role='NA',
                                 location='NA',
                                 job_type='NA',
                                 date_posted=None,
                                 date_closing=None,
                                 company_id=comp.id,
                                 url=i.find('a', {'class': 'subject'})['href'])
        print('Nomura Complete')
    
