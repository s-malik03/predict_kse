import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas
import time

dataframe = pandas.read_csv('stock-exchange-kse-100pakistan.csv')


def getstat(soup_obj):
    stat_type = soup_obj.find_all('div', class_='stats_label')
    stat = soup_obj.find_all('div', class_='stats_value')
    stat_type = [''.join(s.text) for s in stat_type]
    stat = [''.join(s.text) for s in stat]
    openstockval = soup_obj.find('h1', class_='marketIndices__price')
    openstockval = openstockval.text.split(' ')[0]
    closestock = stat[stat_type.index('Previous Close')]
    high = stat[stat_type.index('High')]
    low = stat[stat_type.index('Low')]
    volume = stat[stat_type.index('Volume')]

    return {'Open': openstockval, 'Close': closestock, 'High': high, 'Low': low, 'Volume': volume}


if __name__ == '__main__':
    prev_date = ''
    while True:

        psx_page = requests.get('https://dps.psx.com.pk/')
        soup = BeautifulSoup(psx_page.content, 'html.parser')
        current_date_str = datetime.now().strftime("%d-%b-%y")
        if current_date_str != prev_date:
            openstock = None
            close = None

        current_time = soup.find('div', class_='topbar__status__label').text
        current_datetime = current_time
        current_time = current_time.split(' ')
        ampm = current_time[-1]
        current_time = current_time[3].split(':')

        if ampm == "AM":

            if int(current_time[0]) >= 9 and int(current_time[1]) >= 32:

                if openstock is None:
                    stats = getstat(soup)
                    openstock = stats['Open']
                    print(current_datetime)
                    print("GOT OPENING PRICE: " + openstock)

        elif ampm == "PM":

            if int(current_time[0]) >= 4 and int(current_time[1]) >= 15:

                stats = getstat(soup)
                close = stats['Open']
                print(current_datetime)
                print("GOT CLOSING PRICE: " + close)

                if current_date_str not in list(dataframe['Date']) and openstock is not None:
                    newdata = []
                    newdata.insert(0,
                                   {'Date': current_date_str,
                                    'Open': openstock,
                                    'High': stats["High"],
                                    'Low': stats["Low"],
                                    'Close': close, 'Change': 0,
                                    'Volume': stats["Volume"]})
                    print("SAVING")
                    print(newdata)
                    dataframe = pandas.concat([pandas.DataFrame(newdata), dataframe], ignore_index=True)
                    dataframe.to_csv('stock-exchange-kse-100pakistan.csv', index=False)

        time.sleep(3600)
        prev_date = current_date_str
