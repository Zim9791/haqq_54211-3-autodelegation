# idep-sanford-autodelegation
IDEP Sanford Autodelegation

The script will automatically perform the calls for withdrawing the rewards and send the
necessary transactions to delegate to the validator. The bot uses telegram for notifications
and will provide information on the transaction hashes.


When executing the script, if the password is not in the `IDEP_PASSWORD` environmental variable, the prompt will request a password for the wallet. The password is necessary for the delegation and reward transactions.

The config.ini can be used for loading in the variables or the user's environmental variables may be utilized.

Environmental Variables:
`CHAIN_ID`: Chain ID
`WALLET_NAME`: Wallet Name
`WALLET_KEY`: Wallet Public Key
`VALIDATOR_KEY`: Validator Public Key
`IDEP_PASSWORD`: Wallet Password
`TELEGRAM_TOKEN`: Telegram Token
`TELEGRAM_CHAT_ID`: Telegram Chat ID

Refer to the config.ini.example for a template to populate.

Assumptions:
- iond is in the path of the user
- nominal transaction path only

Install from the requirements file:
```pip3 install -r requirements.txt```

Copy and populate the config.ini file with the necessary information.
```cp config.ini.example config.ini```

Run the script and enter the password
```python3 ./idep-sanford-autodelegation.py```
