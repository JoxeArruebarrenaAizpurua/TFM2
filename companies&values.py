import requests, bs4, numpy, csv, datetime

with open('companiesList.csv', newline='') as file:
    reader = csv.reader(file)
    companiesList = list(reader)

counter = 0
for i in companiesList:
    companiesData = i
    if counter == 0:
        newInfo = (('Date', 'Open', 'High', 'Low', 'Close', 'Volume'))
        companiesData.extend(newInfo)
        counter += 1
    else:
        timestamp = str(int(datetime.datetime.now().timestamp()))
        url = 'https://es.finance.yahoo.com/quote/' + i[1] + '/history?period1=946681201&period2=' + timestamp + '&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'

        page = requests.get(url).text
        soup = bs4.BeautifulSoup(page, 'html.parser')

        infoTable = soup.find('table')
        companyInfo = infoTable.find_all('tr')

        dateList = []
        openList =[]
        highList = []
        lowList = []
        closeList = []
        volumeList = []

        for j in range(1, len(companyInfo)):
            info = companyInfo[j].find_all('td')

            dateList.append(info[0].text)
            openList.append(info[1].text)
            highList.append(info[2].text)
            lowList.append(info[3].text)
            closeList.append(info[4].text)
            volumeList.append(info[5].text)

        newInfo = (dateList, openList, highList, lowList, closeList, volumeList)
        companiesData.extend(newInfo)
    



        print ()