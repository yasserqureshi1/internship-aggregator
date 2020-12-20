import requests
from bs4 import BeautifulSoup
import json
from app.models import Companies, Positions, db


class Scraper:
    def __init__(self):
        self.BailleGifford()

    def BailleGifford(self):
        print('Getting new listings from Baille Gifford...')
        exists = Companies.query.filter_by(name='Baille Gifford').first()
        if not exists:
            comp = Companies(name='Baille Gifford', description='Another company', url='baille-gifford')
            db.session.add(comp)
            db.session.commit()
        comp = Companies.query.filter_by(name='Baille Gifford').first()

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

        pos = Positions.query.filter_by(company_id=comp.id).all()
        for i in pos:
            db.session.delete(i)
            db.session.commit()
        for i in output['body']['children'][0]['children'][0]['listItems']:
            pos = Positions.query.filter_by(name=i['title']['instances'][0]['text'], company_id=comp.id).first()
            if not pos:
                new_pos = Positions(name=i['title']['instances'][0]['text'],
                                division='NA',
                                role='NA',
                                location=i['subtitles'][1]['instances'][0]['text'],
                                timescale='NA',
                                company_id=comp.id,
                                url='NA')
                db.session.add(new_pos)
                db.session.commit()


        print('Baille Gifford Complete')


    def Citi(self):
        headers = {'Host': 'jobs.citi.com',
                   'Referer': 'https://jobs.citi.com/search-jobs',
                   'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                                 'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                   'X-Requested-With': 'XMLHttpRequest'}

        data = {'ActiveFacetID': 'Recent+Graduates'}

        url = 'https://jobs.citi.com/search-jobs/results?ActiveFacetID=Recent+Graduates&CurrentPage=1&RecordsPerPage=18' \
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
            print(i.text)
            print('https://jobs.citi.com' + i['href'])
            print(' ')


    def GoldmanSachs(self):
        url = 'https://www.goldmansachs.com/careers/students/programs/programs-list.json'

        html = requests.get(url)
        output = json.loads(html.text)

        for i in output['programs']:
            print(i['title'])
            print(i['region']['name'])
            print('https://www.goldmansachs.com' + i['url'])
            print(' ')


    def JPMorgan(self):
        url = 'https://careers.jpmorgan.com/services/json/careers/gate/programs.json'

        html = requests.get(url)
        output = json.loads(html.text)

        for i in output:
            for j in output[i]:
                print(j['name'])
                print(j['country'])
                print(j['application_url'])
                print(j['end_date'])
                print(' ')


    def MorganStanley(self):
        url = 'https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-3786f0ce9359/candidate/jobboard/vacancy/1' \
              '/adv/?f_Item_Opportunity_13857_lk=765&f_Item_Opportunity_17058_lk=133794&ftq= '

        html = requests.get(url)
        output = BeautifulSoup(html.text, 'html.parser')

        job_list = output.select('tr[class*="search_res details_row"]')
        for i in job_list:
            print(i['data-title'])
            print(i.find('a', {'class': 'subject'})['href'])
            print(' ')


    def Nomura(self):
        url = 'https://nomuracampus.tal.net/vx/lang-en-GB/mobile-0/appcentre-ext/brand-4/xf-5b60ed84bdc9/candidate' \
              '/jobboard/vacancy/1/adv/?f_Item_Opportunity_84825_lk=765&ftq='

        html = requests.get(url)
        output = BeautifulSoup(html.text, 'html.parser')

        job_list = output.select('tr[class*="search_res details_row"]')
        for i in job_list:
            print(i['data-title'])
            print(i.find('a', {'class': 'subject'})['href'])
            print(' ')


    def RBC(self):
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
            print(i['title'])
            print('https://rbccmgraduates.gtisolutions.co.uk/' + i['dynamicstring_ShortName'] + '/' + str(
                i['dbid']) + '/viewdetails')
            print(' ')


    def UBS(self):
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
            print('https://jobs.ubs.com/TGnewUI/Search/home/HomeWithPreLoad?partnerid=' + str(clientid) + '&siteid=' + str(
                siteid) + '&PageType=JobDetails&jobid=' + str(reqid))
            print(' ')


Scraper()