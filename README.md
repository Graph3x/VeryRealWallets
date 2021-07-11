VeryRealWallets is a mockup of a cryptocurrency wallet API. It is still work in progress and it is mostly unpolished.

All data should be formated in json.

Creating a wallet: POST request to /wallets containing owner (string) and balance (int). Server returns wallets API key and wallets id

Geting balance and owners of all wallets: GET request to /wallets

Getting balance and owner of a single wallet: GET request to /wallets/<id>

Deleting a wallet: DELETE request to /wallets/<id> containing wallets API key (string)

Updating a wallet: PUT request to /wallets/<id> containing owner (string), balance (int) and admin key (string) (admin key is "admin")

Transfering funds: POST request to /transfer/<id> containing target (int), transfer (int) and API key (string)
