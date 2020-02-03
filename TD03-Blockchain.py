import requests
import json
import sqlite3

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


#https://api.pro.coinbase.com/products/BTC-USD/candles?start=2015-01-07T23:47:25.201Z
#https://api.pro.coinbase.com/products/BTC-USD/candles?start=2015-11-07T23:47:25.201Z&end=2015-12-07T23:47:25.201Z&granularity=86400


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
        setTableInsert = ("INSERT INTO " + setTableName + """(Id, date, low, high, open, close, volume) VALUES(""" 
        + str(i) + "," + str(data_candle[i][0]) + "," + str(data_candle[i][1]) + ","
        + str(data_candle[i][2]) + "," + str(data_candle[i][3]) + "," + str(data_candle[i][4]) 
        + "," + str(data_candle[i][5]) + ")")
        print(setTableInsert)
        c.execute(setTableInsert)
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
        print("8. Store the data in sqlite")
        choice = int(input())
        while(choice != 1 and choice !=2 and choice !=3 and choice !=4 and choice !=5 and choice !=6 and choice !=7 and choice !=8 ):
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
    




