import requests
from bs4 import BeautifulSoup
import json
from app.models import Companies, Positions, db


def company_checker(name, description, url):
    """
    This checks whether the company profile is in the db (creates it if not) and deletes all position entries in that company.
    """
    exists = Companies.query.filter_by(name=name).first()  # Checks if company exists in db
    if not exists:  # Adds to db
        comp = Companies(name=name, description=description, url=url)
        db.session.add(comp)
        db.session.commit()
    comp = Companies.query.filter_by(name=name).first()

    pos = Positions.query.filter_by(
        company_id=comp.id).all()  # Deletes all entries for particular company (Prepping for new entries)
    for i in pos:
        db.session.delete(i)
        db.session.commit()
    return comp


def insert_new_positions(name, division, role, location, timescale, company_id, url):
    """
    Inserts new company positions into db
    """
    pos = Positions.query.filter_by(name=name, company_id=company_id).first()
    if not pos:
        new_pos = Positions(name=name,
                            division=division,
                            role=role,
                            location=location,
                            timescale=timescale,
                            company_id=company_id,
                            url=url)
        db.session.add(new_pos)
        db.session.commit()


def check_role(text):
    text = text.lower()
    if 'summer' in text:
        return 'Summer Internship'
    elif '12' or 'placement' or 'year' in text:
        return 'Placement'
    elif 'graduate' or 'full time' in text:
        return 'Graduate'


class Scraper:
    def __init__(self):
        #self.BailleGifford()
        self.Citi()
        #self.MorganStanley()
        #self.JPMorgan()
        #self.GoldmanSachs()
        #self.Nomura()
        #self.Royal_Bank_of_Canada()
        #self.UBS()

    def BailleGifford(self):
        print('Getting new listings from Baille Gifford...')
        comp = company_checker(name='Baille Gifford', description='Another company', url='baille-gifford')

        headers = {
            'User-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'X-Workday-Client': '2020.35.027',
            'Host': 'bailliegifford.wd3.myworkdayjobs.com',
            'Accept': 'application/json,application/xml',
            'workday-client-manifest-id': 'mvp',
            'Referer': 'https://bailliegifford.wd3.myworkdayjobs.com/en-US/BaillieGiffordEarlyCareers'}

        url = "https://bailliegifford.wd3.myworkdayjobs.com/en-US/BaillieGiffordEarlyCareers"

        html = requests.get(url=url, headers=headers)
        output = json.loads(html.text)
        try:
            for i in output['body']['children'][0]['children'][0]['listItems']:
                insert_new_positions(name=i['title']['instances'][0]['text'],
                                     division='NA',
                                     role='NA',
                                     location=i['subtitles'][1]['instances'][0]['text'],
                                     timescale='NA',
                                     company_id=comp.id,
                                     url='NA')
        except:
            insert_new_positions(name='No Roles Found',
                                 division='',
                                 role='',
                                 location='',
                                 timescale='',
                                 company_id=comp.id,
                                 url='')
        print('Baille Gifford Complete')

    def Citi(self):
        print('Getting new listings from Citi Bank...')
        #comp = company_checker(name='Citi', description='Another company', url='citi')

        headers = {'Host': 'jobs.citi.com',
                   'Referer': 'https://jobs.citi.com/search-jobs',
                   'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                                 'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                   'X-Requested-With': 'XMLHttpRequest'}

        data = {'ActiveFacetID': 'Recent+Graduates'}

        url = 'https://jobs.citi.com/search-jobs/results?ActiveFacetID=Recent+Graduates&CurrentPage=1&RecordsPerPage=50' \
              '&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&CustomFacetName=&FacetTerm=&FacetType=0' \
              '&FacetFilters%5B0%5D.ID=2635167&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=18&FacetFilters' \
              '%5B0%5D.Display=United+Kingdom&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName' \
              '=&FacetFilters%5B1%5D.ID=University+Programs&FacetFilters%5B1%5D.FacetType=5&FacetFilters%5B1%5D.Count=15' \
              '&FacetFilters%5B1%5D.Display=University+Programs&FacetFilters%5B1%5D.IsApplied=true&FacetFilters%5B1%5D' \
              '.FieldName=custom_fields.ELIGIBLE_CAMPUS&SearchResultsModuleName=Search+Results&SearchFiltersModuleName' \
              '=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf= '

        html = requests.get(url=url, headers=headers)
        output = json.loads(html.text)

        soup = BeautifulSoup(output['results'], 'html.parser')
        job_list = soup.select('a[data-job-id*=""]')
        for i in job_list:
            split = [j for j in i.text.split('\n') if j != '']
            title = split[0]
            location = split[1]
            #print('gi:', i.text.split('\n'))
            print('https://jobs.citi.com' + i['href'])
            print(' ')
            #insert_new_positions(name=i.text,
            #                     division='NA',
            #                     role='NA',
            #                     location=i['subtitles'][1]['instances'][0]['text'],
            #                     timescale='NA',
            #                     company_id=comp.id,
            #                     url='NA')

    def GoldmanSachs(self):
        print('Getting new listings from Goldman Sachs...')
        comp = company_checker(name='Goldman Sachs', description='Description to be filled', url='goldman-sachs')

        url = 'https://www.goldmansachs.com/careers/students/programs/programs-list.json'

        html = requests.get(url)
        output = json.loads(html.text)

        for i in output['programs']:
            insert_new_positions(name=i['title'],
                                 division='NA',
                                 role='NA',
                                 location=i['region']['name'],
                                 timescale='NA',
                                 company_id=comp.id,
                                 url=f'https://www.goldmansachs.com{i["url"]}')
        print('Goldman Sachs Complete')

    def JPMorgan(self):
        print('Getting new listings from JP Morgan...')
        comp = company_checker(name='J.P. Morgan', description='Description to be filled', url='jp-morgan')

        url = 'https://careers.jpmorgan.com/services/json/careers/gate/programs.json'

        html = requests.get(url)
        output = json.loads(html.text)

        for i in output:
            for j in output[i]:
                insert_new_positions(name=j['title'],
                                     division='NA',
                                     role=j['level'],
                                     location=j['region'],
                                     timescale='NA',
                                     company_id=comp.id,
                                     url=j['application_url'])
            print('JP Morgan Complete')

    def MorganStanley(self):
        print('Getting new listings from Morgan Stanley...')
        comp = company_checker(name='Morgan Stanley', description='Description to be filled', url='morgan-stanley')

        url = 'https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-3786f0ce9359/candidate/jobboard/vacancy/1' \
              '/adv/?f_Item_Opportunity_13857_lk=765&f_Item_Opportunity_17058_lk=133794&ftq= '

        html = requests.get(url)
        output = BeautifulSoup(html.text, 'html.parser')

        job_list = output.select('tr[class*="search_res details_row"]')
        for i in job_list:
            insert_new_positions(name=i['data-title'],
                                 division='NA',
                                 role='NA',
                                 location='NA',
                                 timescale='NA',
                                 company_id=comp.id,
                                 url=i.find('a', {'class': 'subject'})['href'])
        print('Morgan Stanley Complete')

    def Nomura(self):
        print('Getting new listings from Nomura...')
        comp = company_checker(name='Nomura', description='Description to be filled', url='nomura')

        url = 'https://nomuracampus.tal.net/vx/lang-en-GB/mobile-0/appcentre-ext/brand-4/xf-5b60ed84bdc9/candidate' \
              '/jobboard/vacancy/1/adv/?f_Item_Opportunity_84825_lk=765&ftq='

        html = requests.get(url)
        output = BeautifulSoup(html.text, 'html.parser')

        job_list = output.select('tr[class*="search_res details_row"]')
        for i in job_list:
            insert_new_positions(name=i['data-title'],
                                 division='NA',
                                 role='NA',
                                 location='NA',
                                 timescale='NA',
                                 company_id=comp.id,
                                 url=i.find('a', {'class': 'subject'})['href'])
        print('Nomura Complete')

    def Royal_Bank_of_Canada(self):
        print('Getting new listings from Royal Bank of Canada...')
        comp = company_checker(name='Royal Bank of Canada', description='Description to be filled',
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
                                 division='NA',
                                 role='NA',
                                 location='NA',
                                 timescale='NA',
                                 company_id=comp.id,
                                 url=f'https://rbccmgraduates.gtisolutions.co.uk/{i["dynamicstring_ShortName"]}/{i["dbid"]}/viewdetails')
        print('Royal Bank of Canada Complete')

    def UBS(self):
        print('Getting new listings from UBS...')
        comp = company_checker(name='UBS', description='Description to be filled', url='ubs')

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
                                 division='NA',
                                 role='NA',
                                 location='NA',
                                 timescale='NA',
                                 company_id=comp.id,
                                 url=i.find('a', {'class': 'subject'})['href'])
        print('Nomura Complete')


Scraper()