import requests
from bs4 import BeautifulSoup
import nums_from_string
import re
from tqdm import tqdm
from selenium import webdriver
from datetime import date
today = date.today()
def link_scrapper():
    DRIVER_PATH = 'chromeWebDriver/chromedriver.exer'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get('https://www.optioncarriere.com/recherche/emplois?s=&l=France')
    #page = requests.get('https://www.optioncarriere.com/recherche/emplois?s=&l=France',headers={"User-Agent":"Mozilla/5.0"}, proxies = {'http': 'https://51.159.115.233:3128'} )
    page = driver.page_source
    #print(page)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page,'html.parser')
    #print(soup)
    text = soup.find('p',{'class':'col col-xs-12 col-m-4 col-m-r cr'}).find('span').get_text().strip().replace(' ','')
    #text = soup.find('p', string="offres d'emploi").get_text().strip().replace(' ','')
    nbr_page = int(nums_from_string.get_nums(text)[0]/20)

    driver.quit()
    links = []
    titles = []
    for i in range(0,19):
        links.append(soup.find_all('article')[i].find('a')['href'])
        titles.append(soup.find_all('article')[i].find('a')['title'])

    for i in range(0,nbr_page):
        print(i)
        url = 'https://www.optioncarriere.com/emplois-france-57.html?p='+str(i)
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(url)
        page = driver.page_source
        #page = requests.get(url)
        if '{"status":403,"status_msg":"forbidden"}' not in page:
            # Create a BeautifulSoup object
            soup = BeautifulSoup(page, 'html.parser')
            for i in range(0, 19):
                links.append(soup.find_all('article')[i].find('a')['href'])
                titles.append(soup.find_all('article')[i].find('a')['title'])
        else:
            break
    driver.quit()
    return links, titles

def scarp_documents():
    DRIVER_PATH = 'chromeWebDriver/chromedriver.exer'
    links, titles = link_scrapper()
    jobs = []
    for link in tqdm(links):
        link = 'https://www.optioncarriere.com'+link
        print(link)
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(link)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        title = soup.find('h1').get_text()
        if soup.find('p', {'class': 'company'}):
            entreprise = soup.find('p', {'class': 'company'}).get_text()
        else:
            entreprise = ''
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
               'company': entreprise.strip(),
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
        driver.quit()
    return jobs