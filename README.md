# TD03-Blockchain-Programming

# Tasks list - GET

Explanation of def for the GET part:

**#def getCryptoList():**
> Get a list of available currency pairs for trading.
 
**#def getPair():**
> Get a list of available currency pairs for trading.
 
**#def getDepth(direction, pair)**
> Get a list of open orders for a product. The amount of detail shown can be customized with the level parameter.
  In this case, with level 1 we only get the best bid and ask
  
**#def getOrderBook(pair):**
> In this case, with level 2 parameter we get top 50 bids and asks (aggregated).

**#def refreshDataCandle(pair, duration)**
> Historic rates for a product. Rates are returned in grouped buckets based on requested granularity.
  The granularity field must be one of the following values: {60, 300, 900, 3600, 21600, 86400}.

**#def refreshData(pair):**
> List the latest trades for a product.

**#def create_candle_table(setTableName):**
> Here, we create a function wich create a table (if not exist yet) in order to store candles data.

**#def store_candle(setTableName, pair, duration):**
> In this function, we insert or replace into the table created before candles data.
  We create a connection and commit each "tuples".

**#def trackupdates(setTableName,setTableName1, pair, duration):**
> We get the first_date in our previous candle dataset (the most recent). Then we get the           current_date
  and we do the difference between those dates. We convert the difference between those dates in    seconds. Then, we calculate the number of loop needed (in function of the granularity chosen by the user) and get candles data. Then we create the check_updates table and insert candles data.

**#def refreshDataSQlite(setTableName, pair):**
> Store the trade data in SQlite

**#Dictionnary**
> They are used in the main, easier to choose pair, duration and display data.
  
# Tasks list - POST
  
## 9. Create an order
In this part, the user has to enter three parameters of his **Coinbase Pro Sandbox** account (https://public.sandbox.pro.coinbase.com):
- his API Key
- his API Secret Key
- his Passphrase

The code begins by authenticating the user account using these three pieces of information. Then, it displays the current user's **iso** 
and **epoch** to show that the connection is well established with his Coinbase Pro Sandbox account and that the request is correct.
Next, it displays the list trading accounts from the profile of the API key.

       GET /accounts
The command to create an order does not work, the program displays the default values with which we have tested it but the output is:

       POST /orders
       {'message': 'invalid signature'}
Indeed, we did not succeed to find the correct signature to create an order.
The program ends up showing the **list of current open orders** from the profile that the API key belongs to.


## 10. Cancel an order
The beginning of this part is exactly the same as before with the *three needed parameters*.
Then, the code displays the **initial list of orders** from the profile of the API key.

       r = requests.get('https://api-public.sandbox.pro.coinbase.com/orders', auth=auth)
Next, it asks the user to **enter the order ID** he wants to cancel and delete it.
After that, it displays the list of orders again to show that the selected order has disappeared.

# Main

The main is composed of 10 methods, to choose one just enter a number between 1 and 10 include.
After each execution of the loop, you have to press 1 or 2. 
1 to execute an other function and 2 in order to leave the program.

Enjoy :) ! 

V&V
