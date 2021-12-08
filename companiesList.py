import requests, bs4, numpy, csv  #json, pickle, time, csv

def ibex35MembersInfoExtract(companiesList):
    url = 'https://www.bolsamadrid.es/esp/aspx/Mercados/Precios.aspx?indice=ESI100000000&punto=indice'

    page = requests.get(url).text
    soup = bs4.BeautifulSoup(page, 'html.parser')

    companiesTable = soup.find(id='ctl00_Contenido_tblAcciones')
    companies = companiesTable.find_all('tr')

    for i in range(1, len(companies)):
        companyInfo = []
        urlCompany = 'https://www.bolsamadrid.es' + companies[i].find('a').attrs['href']
        
        pageCompany = requests.get(urlCompany).text
        soupCompany = bs4.BeautifulSoup(pageCompany, 'html.parser')

        companyTable = soupCompany.find(id='ctl00_Contenido_CabEmisora_tblEmisora')
        
        try:
            corporativeName = companyTable.find_all('th')[1].string
        except:
            corporativeName = companyTable.find('th').string
        
        companyInfo.append(corporativeName)

        tickerTable = soupCompany.find(id='ctl00_Contenido_tblValor')
        ticker = tickerTable.find(id='ctl00_Contenido_TickerDat').string[:-1] + '.MC'
        
        companyInfo.append(ticker)
        companiesList.append(companyInfo)
    
    return companiesList

def nasdaqMembersInfoExtract(companiesList):
    url = 'https://es.tradingview.com/symbols/NASDAQ-NDX/components/'

    page = requests.get(url).text
    soup = bs4.BeautifulSoup(page, 'html.parser')

    companiesTable = soup.find('table')
    companies = companiesTable.find_all('tr')

    for i in range(1, len(companies)):
        companyInfo = []
        
        corporativeName = companies[i].find('td').attrs['title'].upper()
        companyInfo.append(corporativeName)

        ticker = companies[i].find('td').find('a').text
        companyInfo.append(ticker)

        companiesList.append(companyInfo)

    return companiesList

def sp500MembersInfoExtract(companiesList):
    url = 'https://esbolsa.com/blog/bolsa-americana/que-es-el-sp-500/'

    page = requests.get(url).text
    soup = bs4.BeautifulSoup(page, 'html.parser')

    companiesTable = soup.find('table')
    companies = companiesTable.find_all('tr')

    counter = 0
    while counter < 3:
        for i in range(1, len(companies)):
            companyInfo = []
            
            corporativeName = companies[i].find_all('td')[1 + counter].text.upper()
            if corporativeName != '':
                companyInfo.append(corporativeName)

            ticker = companies[i].find_all('td')[counter].text
            if ticker != '':
                companyInfo.append(ticker)

            if len(companyInfo) != 0:
                companiesList.append(companyInfo)
        
        counter += 2
    
    return companiesList

""" companiesList = [['Corporative Name', 'Ticker']]
ibex35MembersInfoExtract(companiesList)
nasdaqMembersInfoExtract(companiesList)
sp500MembersInfoExtract(companiesList)

companiesList.sort(key=lambda company: company[1]) """

with open('companiesList.csv', newline='') as file:
    reader = csv.reader(file)
    companiesList = list(reader)

finalCompaniesList = []
notAvailableList = ['BRK.B', 'CTL', 'BF.B', 'CXO', 'ETFC', 'MYL', 'NBL', 'TIF', 'WRK', 'FOX']
for i in companiesList:
    if len(finalCompaniesList) == 0:
        finalCompaniesList.append(i)
    else:
        contador = 1
        for j in finalCompaniesList:
            if i[1] == j[1] or i[1] in notAvailableList:
                break
            elif contador == len(finalCompaniesList):
                finalCompaniesList.append(i)
                break
            else:
                contador += 1

#finalCompaniesList.insert(0, ['Corporative Name', 'Ticker'])


with open('companiesList.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(finalCompaniesList)
