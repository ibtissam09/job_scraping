import requests
from bs4 import BeautifulSoup
import nums_from_string
import re
from tqdm import tqdm
from datetime import date
today = date.today()
def link_scrapper():
    page = requests.get('https://www.optioncarriere.ma/recherche/emplois?s=&l=')
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text,'html.parser')
    text = soup.find('p',{'class':'col col-xs-12 col-m-4 col-m-r cr'}).find('span').get_text().strip().replace(' ','')
    nbr_page = int(nums_from_string.get_nums(text)[0]/20)
    #print(text)
    links = []
    titles = []
    for i in range(0,19):
        links.append(soup.find_all('h2')[i].find('a')['href'])
        titles.append(soup.find_all('h2')[i].find('a')['title'])
    for i in range(0,nbr_page):
        url = 'https://www.optioncarriere.ma/emplois-maroc-113535.html?p='+str(i)
        page = requests.get(url)
        if page.status_code == 200:
            # Create a BeautifulSoup object
            soup = BeautifulSoup(page.text, 'html.parser')
            for i in range(0, 19):
                links.append(soup.find_all('h2')[i].find('a')['href'])
                titles.append(soup.find_all('h2')[i].find('a')['title'])
        else:
            break
    return links, titles

def scarp_documents():
    links, titles = link_scrapper()
    jobs = []
    for link in tqdm(links):
        link = 'https://www.optioncarriere.ma/'+link
        print(link)
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        title = soup.find('h1').get_text()
        if soup.find('p', {'class': 'company'}):
            entreprise = soup.find('p', {'class': 'company'}).get_text().strip()
        else:
            entreprise = None
        details = []
        for d in soup.find('ul', {'class': 'details'}).find_all('li'):
            details.append(d.get_text())
        tags = []
        for d in soup.find('ul', {'class': 'tags'}).find_all('li'):
            tags.append(d.get_text())
        description = soup.find('section', {'class': 'content'}).get_text()
        phrases = [li.get_text() for li in soup.find('section', {'class': 'content'}).find_all('li')]
        if soup.find('b', text=re.compile("(M|m)ission")):
            if soup.find('b', text=re.compile("(M|m)ission")).find_next_sibling('ul'):
                missions = soup.find('b', text=re.compile("(M|m)ission")).find_next_sibling('ul').find_all('li')
                missions = [li.get_text() for li in missions]
            else:
                missions = []
        else:
            missions =[]
        if soup.find('b', text=re.compile("(P|p)oste")):
            if soup.find('b', text=re.compile("(P|p)oste")).find_next_sibling('ul'):
                poste = soup.find('b', text=re.compile("(P|p)oste")).find_next_sibling('ul').find_all('li')
                poste = [li.get_text() for li in poste]
            else:
                poste = []
        else:
            poste = []
        if soup.find('b', text=re.compile("(P|p)rofil")):
            if soup.find('b', text=re.compile("(P|p)rofil")).find_next_sibling('ul'):
                #print(soup.find('b', text=re.compile("(P|p)rofil")))
                profil = soup.find('b', text=re.compile("(P|p)rofil")).find_next_sibling('ul').find_all('li')
                profil = [li.get_text() for li in profil]
            else:
                profil = []
        else:
            profil = []
        job = {'link': link,
               'title': title.strip(),
               'company': entreprise,
               'details': details,
               'tags': tags,
               'description': { 'desc' : description,
                                'values':{'mission':missions,
                                          'profile':profil,
                                          'poste':poste
                                          },
                                'phrases': phrases,
                                },
               "insert_time": today.strftime("%d/%m/%Y"),
               "DUP": "D"
               }
        jobs.append(job)
    return jobs