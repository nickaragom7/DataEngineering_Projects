import requests

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=70H117QUS6AVTGV5'

r = requests.get(url)

data = r.json()

print(data)