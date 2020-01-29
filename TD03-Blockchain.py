import requests

import json
response = requests.get("https://api.pro.coinbase.com/products")
data = response.json()
for i in range(len(data)):
    currencies = data[i]['base_currency']
    print(i,':', currencies)



def getDepth(direction, pair):
    link = ['https://api.pro.coinbase.com/products/', pair, '/book']
    link = "".join(link)
    response = requests.get(link)
    book = response.json()
    print('The', direction, 'price for', pair, 'is:', book[direction][0][0:2])

getDepth('asks', 'BTC-USD')

def getOrderBook(pair):  
    link = ['https://api.pro.coinbase.com/products/', pair, '/book?level=2'] #Top 50 bids and asks (aggregated), for Full Order Book level =3.
    link = "".join(link)
    response = requests.get(link)
    book = response.json()
    for i in range(len(book['bids'])):
        print('bids ', i+1 , ':', book['bids'][i][0:2], ' asks', i+1, ':', book['asks'][i][0:2])
    
    

#getOrderBook('BTC-USD')

