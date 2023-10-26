import requests
import gspread
from datetime import datetime
from time import sleep

def getCurrencyFromBankApi(startDate: str, endDate: str):
    startDate = startDate.replace('-', '')
    endDate = endDate.replace('-', '')
    url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={startDate}&end={endDate}&valcode=usd&sort=exchangedate&order=asc&json'
    response = requests.get(url=url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def writeResToGoogleSheet(currencyToWriter: list):
   googleSheet = gspread.service_account(filename='path/to/creds')
   sheet = googleSheet.open('sheetname')
   sheet.values_clear("A2:B1000")
   worksheet = sheet.sheet1
   for i in range(0, len(currencyToWriter)):
        acellIndex = i+2
        date = currencyToWriter[i]['exchangedate']
        rate = currencyToWriter[i]['rate']
        rate = int(rate)
        if rate > 1000:
            rate = rate/100.0
        try:
            worksheet.update_acell(f'A{acellIndex}', date)
        except gspread.exceptions.APIError:
            sleep(60)
            googleSheet.session.close()
            googleSheet = gspread.service_account(filename='path/to/creds')
            sheet = googleSheet.open('sheetname')
            worksheet = sheet.sheet1
            worksheet.update_acell(f'A{acellIndex}', date)
        
        try:
            worksheet.update_acell(f'B{acellIndex}', 
                                str(rate).replace('.', ','))
        except gspread.exceptions.APIError:
            sleep(60)
            googleSheet.session.close()
            googleSheet = gspread.service_account(filename='path/to/creds')
            sheet = googleSheet.open('sheetname')
            worksheet = sheet.sheet1
            worksheet.update_acell(f'B{acellIndex}', 
                                str(rate).replace('.', ','))





