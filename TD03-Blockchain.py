import requests
import json
import sqlite3
import pytz
from datetime import datetime
import dateutil.parser as dp
from math import *
import hmac, hashlib, time
from requests.auth import AuthBase
import base64

def getCryptoList():
    response = requests.get("https://api.pro.coinbase.com/products")
    data = response.json()
    for i in range(len(data)):
        currencies = data[i]['base_currency']
        print(i,':', currencies)

def getPair():
    response = requests.get("https://api.pro.coinbase.com/products")
    data = response.json()
    for i in range(len(data)):
        pair = data[i]['id']
        print(i,':', pair)

def getDepth(direction, pair):
    link = ['https://api.pro.coinbase.com/products/', pair, '/book']
    link = "".join(link)
    response = requests.get(link)
    book = response.json()
    print('The', direction, 'price for', pair, 'is:', book[direction][0][0])

def getOrderBook(pair):  
    link = ['https://api.pro.coinbase.com/products/', pair, '/book?level=2'] #Top 50 bids and asks (aggregated), for Full Order Book level =3.
    link = "".join(link)
    response = requests.get(link)
    book = response.json()
    for i in range(len(book['bids'])):
        print('bids ', i+1 , ':', book['bids'][i][0:2], ' asks', i+1, ':', book['asks'][i][0:2])

def refreshDataCandle(pair, duration):
    link = ['https://api.pro.coinbase.com/products/', pair, '/candles?granularity=', duration] #Top 50 bids and asks (aggregated), for Full Order Book level =3.
    link = "".join(link)
    response = requests.get(link)
    candle = response.json()
    print(candle)
    return candle

def refreshData(pair):
    link = ['https://api.pro.coinbase.com/products/', pair, '/trades'] #Top 50 bids and asks (aggregated), for Full Order Book level =3.
    link = "".join(link)
    response = requests.get(link)
    trades = response.json()
    return trades

def create_candle_table(setTableName):

    conn = sqlite3.connect(setTableName)
    c = conn.cursor()

    tableCreationStatement = "CREATE TABLE IF NOT EXISTS " + setTableName + """(Id INTEGER PRIMARY KEY, date INT, low REAL,
    high REAL, open REAL, close REAL, volume REAL)"""
    c.execute(tableCreationStatement)

    print("Table successfully created !")
    c.close()
    conn.close()

def store_candle(setTableName, pair, duration): #create candles_table
    
    conn = sqlite3.connect(setTableName)
    c = conn.cursor()

    tableCreationStatement = "CREATE TABLE IF NOT EXISTS " + setTableName + """(Id INTEGER PRIMARY KEY, date INT, low REAL,
    high REAL, open REAL, close REAL, volume REAL)"""
    c.execute(tableCreationStatement)
    data_candle = refreshDataCandle(pair, duration)

    for i in range(len(data_candle)):
        setTableInsert = ("INSERT OR REPLACE INTO " + setTableName + """(Id, date, low, high, open, close, volume) VALUES(""" 
        + str(i) + "," + str(data_candle[i][0]) + "," + str(data_candle[i][1]) + ","
        + str(data_candle[i][2]) + "," + str(data_candle[i][3]) + "," + str(data_candle[i][4]) 
        + "," + str(data_candle[i][5]) + ")")
        print(setTableInsert)
        c.execute(setTableInsert)
        conn.commit()
    
    c.close()
    conn.close()

def trackupdates(setTableName,setTableName1, pair, duration):
    
    conn = sqlite3.connect(setTableName)
    c = conn.cursor()
    c.execute('SELECT MAX(date) ' + 'FROM ' + setTableName ) #Dernière date_enregistrée (dernier tuple) -> MAX
    first_date = c.fetchone()
    first_date = int(first_date[0])
    tz = pytz.timezone('Europe/Paris')
    first_date = datetime.fromtimestamp(first_date, tz).isoformat() 
    str(first_date)
    current_date = str(datetime.now())
    first_date = first_date[:10] + 'T' + first_date[11:19] + '.201Z'
    current_date = current_date[:10] + 'T' + current_date[11:20]+'201Z'
    #Convert to DateTime
    previous_date = datetime(int(first_date[:4]),int(first_date[5:7]), int(first_date[8:10]), int(first_date[11:13]), int(first_date[14:16]),int(first_date[17:19]))
    atm_date = datetime(int(current_date[:4]), int(current_date[5:7]), int(current_date[8:10]), int(current_date[11:13]), int(current_date[14:16]), int(current_date[17:19]))
    duree = atm_date - previous_date
    duree = duree.seconds
    
    nbr_rq = floor(duree/(300*int(duration)))
  
    updates = []
    for i in range(nbr_rq + 1):
        if(i == 0):
            link = ['https://api.pro.coinbase.com/products/', pair, '/candles?start='+ first_date + '&granularity=' + duration]
            link = "".join(link)
            response = requests.get(link)
            updates.extend(response.json())
            #print("START")
        elif(i == nbr_rq):
            link = ['https://api.pro.coinbase.com/products/', pair, '/candles?end='+ current_date +'&granularity=' + duration]
            link = "".join(link)
            response = requests.get(link)
            updates.extend(response.json())
            #print("LAST")
        else:
            link = ['https://api.pro.coinbase.com/products/', pair, '/candles?granularity=' + duration]
            link = "".join(link)
            response = requests.get(link)
            updates.extend(response.json())
            #print("MID")
    
    conn = sqlite3.connect(setTableName1)
    c = conn.cursor()

    tableCreationStatement = "CREATE TABLE IF NOT EXISTS " + setTableName1 + """(Id INTEGER PRIMARY KEY, date INT, low REAL,
    high REAL, open REAL, close REAL, volume REAL)"""
    c.execute(tableCreationStatement)

    for i in range(len(updates)):
        setTableInsert = ("INSERT OR REPLACE INTO " + setTableName1 + """(Id, date, low, high, open, close, volume) VALUES(""" 
        + str(i) + "," + str(updates[i][0]) + "," + str(updates[i][1]) + ","
        + str(updates[i][2]) + "," + str(updates[i][3]) + "," + str(updates[i][4]) 
        + "," + str(updates[i][5]) + ")")
        print(setTableInsert)
        c.execute(setTableInsert)
        conn.commit() 
    c.close()
    conn.close()

# Create custom authentication for Coinbase API
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = (timestamp + str(request.method) + str(request.path_url) + str(request.body or ''))
        message = message.encode('ascii')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())        

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

def createOrder(api_key, secret_key, passphrase, direction, price, amount, pair, orderType):
    api_url = 'https://api-public.sandbox.pro.coinbase.com/'
    auth = CoinbaseExchangeAuth(api_key, secret_key, passphrase)

    # Get current user
    r = requests.get(api_url + 'time', auth=auth)
    print('\nCurrent user:', r.json())

    # Show accounts
    r = requests.get(api_url + 'accounts', auth=auth)
    print('\nAccounts:', r.json())

    # Place an order
    order = {
        'size': amount,
        'price': price,
        'side': direction,
        'product_id': pair,
    }

    print('\nOrder request:', order)

    r = requests.post(api_url + 'orders', json=order, auth=auth)
    print('\nOrder created:', r.json())

    # Show list of orders
    r = requests.get('https://api-public.sandbox.pro.coinbase.com/orders', auth=auth)
    print('\nList of orders:', r.json())

def cancelOrder(api_key, secret_key, passphrase, uuid):
    auth = CoinbaseExchangeAuth(api_key, secret_key, passphrase)

    # Cancel an order
    url = ['https://api-public.sandbox.pro.coinbase.com/orders/', uuid]
    url = "".join(url)
    r = requests.delete(url, auth=auth)
    print('Order canceled:', r.json())

def refreshDataSQlite(setTableName, pair):
    conn = sqlite3.connect(setTableName)
    c = conn.cursor()

    tableCreationStatement = "CREATE TABLE IF NOT EXISTS " + setTableName + """(Id INTEGER PRIMARY KEY, 
    traded_btc REAL, price REAL, created_at_int INT, side TEXT)"""

    c.execute(tableCreationStatement)
    data_frame = refreshData(pair)

    for i in range(len(data_frame)):
        setTableInsert = ("INSERT OR REPLACE INTO " + setTableName + """(Id, traded_btc, price, created_at_int, side) 
        VALUES(?,?,?,?,?);""")

        print("INSERT INTO" + setTableName + ":" + str(i) + "," + str(data_frame[i]['trade_id']) + "," + str(data_frame[i]['price']) + "," + data_frame[i]['time'] + "," + data_frame[i]['side'])
        
        c.execute(setTableInsert,(str(i), str(data_frame[i]['trade_id']), str(data_frame[i]['price']), data_frame[i]['time'], data_frame[i]['side']))
        conn.commit() 
    c.close()
    conn.close()

def DictionnaryPair(i):
    switcher={
        0 : 'ZRX-BTC',
        1 : 'BAT-USDC',
        2 : 'DAI-USDC',
        3 : 'BTC-USDC',
        4 : 'XTZ-USD',
        5 : 'MANA-USDC',
        6 : 'OXT-USD',
        7 : 'REP-USD',
        8 : 'XLM-USD',
        9 : 'ETC-USD',
        10 : 'ALGO-USD',
        11 : 'ETC-EUR',
        12 : 'ETH-USDC',
        13 : 'ETH-EUR',
        14 : 'LTC-BTC',
        15 : 'EOS-USD',
        16 : 'BCH-EUR',
        17 : 'BAT-ETH',
        18 : 'XLM-BTC',
        19 : 'ATOM-BTC',
        20 : 'ZEC-BTC',
        21 : 'LINK-ETH',
        22 : 'LTC-EUR',
        23 : 'ETH-BTC',
        24 : 'DASH-USD',
        25 : 'XLM-EUR',
        26 : 'DNT-USDC',
        27 : 'BCH-GBP',
        28 : 'ETH-USD',
        29 : 'LTC-GBP',
        30 : 'DASH-BTC',
        31 : 'ZRX-USD',
        32 : 'BCH-USD',
        33 : 'XTZ-BTC',
        34 : 'XRP-EUR',
        35 : 'XRP-USD',
        36 : 'BTC-GBP',
        37 : 'BCH-BTC',
        38 : 'REP-BTC',
        39 : 'ZEC-USDC',
        40 : 'LOOM-USDC',
        41 : 'ZRX-EUR',
        42 : 'EOS-EUR',
        43 : 'BTC-USD',
        44 : 'LTC-USD',
        45 : 'XRP-BTC',
        46 : 'BTC-EUR',
        47 : 'ATOM-USD',
        48 : 'ETH-GBP',
        49 : 'ETC-BTC',
        50 : 'CVC-USDC',
        51 : 'EOS-BTC',
        52 : 'LINK-USD',
        53 : 'ETH-DAI',
        54 : 'ETC-GBP',
        55 : 'GNT-USDC',
             }
    return switcher.get(i, "Invalid input")

def DictionnaryPairPrint():
            print("""
        0 : ZRX-BTC
        1 : BAT-USDC
        2 : DAI-USDC
        3 : BTC-USDC
        4 : XTZ-USD
        5 : MANA-USDC
        6 : OXT-USD
        7 : REP-USD
        8 : XLM-USD
        9 : ETC-US
        10 : ALGO-USD
        11 : ETC-EUR
        12 : ETH-USDC
        13 : ETH-EUR
        14 : LTC-BTC
        15 : EOS-USD
        16 : BCH-EUR
        17 : BAT-ETH
        18 : XLM-BTC
        19 : ATOM-BTC
        20 : ZEC-BTC
        21 : LINK-ETH
        22 : LTC-EUR
        23 : ETH-BTC
        24 : DASH-USD
        25 : XLM-EUR
        26 : DNT-USDC
        27 : BCH-GBP
        28 : ETH-USD
        29 : LTC-GBP
        30 : DASH-BTC
        31 : ZRX-USD
        32 : BCH-USD
        33 : XTZ-BTC
        34 : XRP-EUR
        35 : XRP-USD
        36 : BTC-GBP
        37 : BCH-BTC
        38 : REP-BTC
        39 : ZEC-USDC
        40 : LOOM-USDC
        41 : ZRX-EUR
        42 : EOS-EUR
        43 : BTC-USD
        44 : LTC-USD
        45 : XRP-BTC
        46 : BTC-EUR
        47 : ATOM-USD
        48 : ETH-GBP
        49 : ETC-BTC
        50 : CVC-USDC
        51 : EOS-BTC
        52 : LINK-USD
        53 : ETH-DAI
        54 : ETC-GBP
        55 : GNT-USDC""")

def DictionnaryGranularity(i):
    switcher={
        1:'60',
        2:'300',
        3:'900',
        4:'3600',
        5:'21600',
        6:'86400',
    }  
    return switcher.get(i, "Invalid input")    

def DictionnaryGranularityPrint():
    print("""
        1: one minute
        2: five minute
        3: fifteen minutes
        4: one hour
        5: six hour
        6: one day

    """)

def DictionnaryPairTable(i):
    switcher={
        0 : 'ZRXBTC',
        1 : 'BATUSDC',
        2 : 'DAIUSDC',
        3 : 'BTCUSDC',
        4 : 'XTZUSD',
        5 : 'MANAUSDC',
        6 : 'OXTUSD',
        7 : 'REPUSD',
        8 : 'XLMUSD',
        9 : 'ETCUSD',
        10 : 'ALGOUSD',
        11 : 'ETCEUR',
        12 : 'ETHUSDC',
        13 : 'ETHEUR',
        14 : 'LTCBTC',
        15 : 'EOSUSD',
        16 : 'BCHEUR',
        17 : 'BATETH',
        18 : 'XLMBTC',
        19 : 'ATOMBTC',
        20 : 'ZECBTC',
        21 : 'LINKETH',
        22 : 'LTCEUR',
        23 : 'ETHBTC',
        24 : 'DASHUSD',
        25 : 'XLMEUR',
        26 : 'DNTUSDC',
        27 : 'BCHGBP',
        28 : 'ETHUSD',
        29 : 'LTCGBP',
        30 : 'DASHBTC',
        31 : 'ZRXUSD',
        32 : 'BCHUSD',
        33 : 'XTZBTC',
        34 : 'XRPEUR',
        35 : 'XRPUSD',
        36 : 'BTCGBP',
        37 : 'BCHBTC',
        38 : 'REPBTC',
        39 : 'ZECUSDC',
        40 : 'LOOMUSDC',
        41 : 'ZRXEUR',
        42 : 'EOSEUR',
        43 : 'BTCUSD',
        44 : 'LTCUSD',
        45 : 'XRPBTC',
        46 : 'BTCEUR',
        47 : 'ATOMUSD',
        48 : 'ETHGBP',
        49 : 'ETCBTC',
        50 : 'CVCUSDC',
        51 : 'EOSBTC',
        52 : 'LINKUSD',
        53 : 'ETHDAI',
        54 : 'ETCGBP',
        55 : 'GNTUSDC',
             }
    return switcher.get(i, "Invalid input")

    
def main():
    while(True):
        print("Hello, please choose a task to run") 
        print("1. Get a list of all available cryptocurrencies and display it")
        print("2. Create a function to display the 'ask' or 'bid' price of an asset")
        print("3. Get order book for an asset")
        print("4. Create a function to read agregated trading data")
        print("5. Create a sqlite table to store said data")
        print("6. Store candle data in the db")
        print("7. Modify function to update when new candle data is available")
        print("8. Extract and store all available data in sqlite")
        print("9. Create an order")
        print("10.Cancel an order")
        choice = int(input())
        while(choice != 1 and choice !=2 and choice !=3 and choice !=4 and choice !=5 and choice !=6 and choice !=7 and choice !=8 and choice != 9 and choice != 10):
            print("Invalid input, please choose a number between 1 and 8")
            choice = int(input())
        if choice == 1:
            getCryptoList()
        elif choice == 2:
            print("Choose a direction :")
            print("1. Asks")
            print("2. Bids")
            direction = int(input())
            while(direction != 1 and direction !=2):
                print("Invalid input, please choose 1 or 2")
                direction = int(input())
            if(direction == 1):
                direction = 'asks'
            else:
                direction = 'bids'
            DictionnaryPairPrint()
            print("Choose a pair (use ctrl + f to find the number easily)")
            pair = DictionnaryPair(int(input())) 
            getDepth(direction,pair)
        elif choice == 3:
            DictionnaryPairPrint()
            print("Choose a pair (use ctrl + f to find the number easily)")
            pair = DictionnaryPair(int(input()))
            getOrderBook(pair)
        elif choice == 4:
            DictionnaryPairPrint()
            print("Choose a pair (use ctrl + f to find the number easily)")
            pair = DictionnaryPair(int(input()))
            DictionnaryGranularityPrint()
            print("Choose the duration")
            duration = DictionnaryGranularity(int(input()))
            refreshDataCandle(pair,duration)
        elif choice == 5:
            DictionnaryPairPrint()
            print("Choose a pair (use ctrl + f to find the number easily)")
            pair = DictionnaryPairTable(int(input()))
            DictionnaryGranularityPrint()
            print("Choose the duration")
            duration = DictionnaryGranularity(int(input()))
            exchangeName = 'Coinbase'
            setTableName = str(exchangeName + "_" + pair + "_" + str(duration))
            create_candle_table(setTableName)
        elif choice == 6:
            DictionnaryPairPrint()
            print("Choose a pair (use ctrl + f to find the number easily)")
            nbr = int(input())
            pair = DictionnaryPairTable(nbr)
            pair_bis = DictionnaryPair(nbr)
            DictionnaryGranularityPrint()
            print("Choose the duration")
            duration = DictionnaryGranularity(int(input()))
            exchangeName = 'Coinbase'
            setTableName = str(exchangeName + "_" + pair + "_" + str(duration))
            store_candle(setTableName, pair_bis, duration)
        elif choice == 7:
            DictionnaryPairPrint()
            print("Choose a pair (use ctrl + f to find the number easily)")
            nbr = int(input())
            pair = DictionnaryPair(nbr)
            pair_bis = DictionnaryPairTable(nbr)
            DictionnaryGranularityPrint()
            print("Choose the duration")
            duration = DictionnaryGranularity(int(input()))
            exchangeName = 'Coinbase'
            print("Entrez le nom de la db que vous souhaitez update")
            setTableName = input()
            setTableName1 = str("last_checks_"+ exchangeName + "_" + pair_bis + "_" + str(duration))
            trackupdates(setTableName, setTableName1, pair, duration)
        elif choice == 8 :
            DictionnaryPairPrint()
            print("Choose a pair (use ctrl + f to find the number easily)")
            nbr = int(input())
            pair = DictionnaryPairTable(nbr)
            pair_bis = DictionnaryPair(nbr)
            exchangeName = 'Coinbase'
            setTableName = str(exchangeName + "_" + pair)
            print(setTableName)
            refreshDataSQlite(setTableName, pair_bis)
        elif choice == 9:
            print('\nEnter your API Key:')
            api_key = bytes(input(), encoding = 'utf-8')
            print('Enter your API Secret Key:')
            secret_key = bytes(input(), encoding = 'utf-8')
            print('Enter your Passphrase:')
            passphrase = bytes(input(), encoding = 'utf-8')

            # Default values
            amount = 1.0
            price = 1.0
            direction = 'buy'
            pair = 'BTC-USD'
            orderType = 'limit'

            createOrder(api_key, secret_key, passphrase, direction, price, amount, pair, orderType)
        elif choice == 10:
            print('\nEnter your API Key:')
            api_key = bytes(input(), encoding = 'utf-8')
            print('Enter your API Secret Key:')
            secret_key = bytes(input(), encoding = 'utf-8')
            print('Enter your Passphrase:')
            passphrase = bytes(input(), encoding = 'utf-8')

            # Show initial list of orders
            auth = CoinbaseExchangeAuth(api_key, secret_key, passphrase)
            r = requests.get('https://api-public.sandbox.pro.coinbase.com/orders', auth=auth)
            print('\nInitial list of orders:', r.json())

            print('\nEnter the order ID you want to cancel:')
            uuid = input()

            cancelOrder(api_key, secret_key, passphrase, uuid)

            # Show final list of orders
            r = requests.get('https://api-public.sandbox.pro.coinbase.com/orders', auth=auth)
            print('\nFinal list of orders:', r.json())

        print("Run again or Exit ?")
        print("1. Run again !")
        print("2. Exit")
        choice = int(input())
        while(choice != 1 and choice !=2):
            print("Invalid input, please choose 1 or 2")
            choice = int(input())
        if choice ==1:
            print("Still running...")
        else: 
            print("Stopping...")
            break

  
main()
    


#https://api.pro.coinbase.com/products/BTC-USD/candles?start=2015-01-07T23:47:25.201Z
#https://api.pro.coinbase.com/products/BTC-USD/candles?start=2019-04-10T02:00:00+201Z&end=2015-12-07T23:47:25.201Z&granularity=86400

