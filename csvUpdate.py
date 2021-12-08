import requests, csv, bs4
from datetime import datetime

with open('companiesList.csv', newline='') as file:
    reader = csv.reader(file)
    companiesList = list(reader)

counter = 0
company = 0
for i in companiesList:
    companiesData = i
    dailyInfoList = []
    if counter != 0 and counter > company:
        with open('Companies_CSV/' + i[1] + '.csv', newline='') as file:
            reader = csv.reader(file)
            historicalInfo = list(reader)

        url = 'https://finance.yahoo.com/quote/'+ i[1] +'/history?p=' + i[1]

        page = requests.get(url).text
        soup = bs4.BeautifulSoup(page, 'html.parser')

        infoTable = soup.find('table')
        tableSections = infoTable.find_all('tr')
        dailyInfo = tableSections[1].find_all('td')

        date = dailyInfo[0].text
        dateDigit = datetime.strptime(date, '%b %d, %Y')
        year = str(dateDigit.year)

        if len(str(dateDigit.month)) == 1:
            month = '0' + str(dateDigit.month)
        else:
            month = str(dateDigit.month)

        if len(str(dateDigit.day)) == 1:
            day = '0' + str(dateDigit.day)
        else:
            day = str(dateDigit.day)

        finalDate = year + '-' + month + '-' + day
        dailyInfoList.append(finalDate)

        openValue = dailyInfo[1].text
        dailyInfoList.append(openValue)

        high = dailyInfo[2].text
        dailyInfoList.append(high)

        low = dailyInfo[3].text
        dailyInfoList.append(low)

        close = dailyInfo[4].text
        dailyInfoList.append(close)

        adjClose = dailyInfo[5].text
        dailyInfoList.append(adjClose)

        volume = dailyInfo[6].text
        dailyInfoList.append(volume)

        historicalInfo.append(dailyInfoList)

        with open('Companies_CSV/' + i[1] + '.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(historicalInfo)

    
    counter += 1

print()  

