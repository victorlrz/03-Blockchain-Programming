# TD03-Blockchain-Programming

# Tasks list - GET

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
The program ends up showing the list of current open orders from the profile that the API key belongs to.


## 10. Cancel an order
The beginning of this part is exactly the same as before with the three needed parameters.
Then, the code displays the initial list of orders from the profile of the API key.

       r = requests.get('https://api-public.sandbox.pro.coinbase.com/orders', auth=auth)
Next, it asks the user to enter the order ID he wants to cancel and delete it.
After that, it displays the list of orders again to show that the selected order has disappeared.
