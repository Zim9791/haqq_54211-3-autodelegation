# idep-sanford-autodelegation
IDEP Sanford Autodelegation

The script will automatically perform the calls for withdrawing the rewards and send the necessary transactions to delegate to the validator. 

The bot will print out the information to both the terminal and send telegram for notifications, if available. The information provided includes the transaction hashes and the delegation amount.

When executing the script, if the password is not in the `IDEP_PASSWORD` environmental variable, it will check the config.ini file for the password variable. If the password is not found in either the environment or in the config.ini, a prompt will request a password for the wallet. The password is necessary for the delegation and reward transactions.

The config.ini can be used for loading in the variables or the user's environmental variables may be utilized.

Environmental Variables:
- `CHAIN_ID`: Chain ID
- `WALLET_NAME`: Wallet Name
- `WALLET_KEY`: Wallet Public Key
- `VALIDATOR_KEY`: Validator Public Key
- `IDEP_PASSWORD`: Wallet Password
- `TELEGRAM_TOKEN`: Telegram Token
- `TELEGRAM_CHAT_ID`: Telegram Chat ID
- `SLEEP_TIME`: Sleep Time for Delegation Cycles

Refer to the config.ini.example for a template to populate.

Assumptions:
- iond is in the path of the user
- nominal transaction path only
- no fees taken into account for the delegation transactions

Install python3 and install from the requirements file:
```pip3 install -r requirements.txt```

Copy and populate the config.ini file with the necessary information.
```cp config.ini.example config.ini```

Run the script
```python3 ./idep-sanford-autodelegation.py```

Example of Output:
```Hello from IDEP Autodelegation Bot on nuremberg!
Start Delegation Cycle!
 - Current Delegation: 1760.27555798 
 - Distribution Tx Hash: 1C95365336438D4442BB4E89AD494DD218E0EC4B03A1DDE6DD5530B40A2C8828
 - Commission Tx Hash: 833667E687ABCF4D0EB7BB5C563CEB787D58E28481AA15452BCD7B0A15287349
 - Current Balance (post distribution): 0.05539889 
 - Delegation Tx Hash: 725D3FABC4F124DBC144A5ADF1DB02D7DDA9282DE9F1CBBEE95D9BBB3DC49081
 - New Delegation: 1760.3309568700001 ( Delta: 0.055398890000105894 )
End Delegation Cycle
Sleeping 3605 Seconds```