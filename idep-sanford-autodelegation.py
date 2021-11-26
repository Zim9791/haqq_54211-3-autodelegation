#!/usr/bin/env python3
import os, requests
import configparser
import pexpect
import getpass
import time 
from subprocess import Popen, PIPE

class IdepAutodelegation():
    def __init__( self, config_file='config.ini' ):
        # obtain the host name
        self.name = os.uname()[1]

        # read the config and setup the telegram
        self.read_config( config_file )
        self.setup_telegram()
        self.setup_idep_info()

        # Prompt for the password
        self.password = getpass.getpass("Enter the wallet password: ")

        # send the hello message
        self.send( f'{self.name}: Hello from IDEP Autodelegation Bot!\nCurrent Delegations: { self.get_delegations() }' )
        
    def read_config( self, config_file ):
        '''
        Read the configuration file
        '''
        config = configparser.ConfigParser()
        config.read( config_file )
        self.config = config

    def setup_telegram( self ):
        '''
        Setup telegram
        '''
        self.telegram_token = self.config['Telegram']['telegram_token']
        self.telegram_chat_id = self.config['Telegram']['telegram_chat_id']

    def setup_idep_info( self ):
        '''
        Setup idep info
        '''
        self.chain_id = self.config['IDEP']['chain_id']
        self.wallet_name = self.config['IDEP']['wallet_name']
        self.wallet_key = self.config['IDEP']['wallet_key']
        self.validator_key = self.config['IDEP']['validator_key']

    def send( self, msg ):
        '''
        Send telegram message
        '''
        requests.post( f'https://api.telegram.org/bot{self.telegram_token}/sendMessage?chat_id={self.telegram_chat_id}&text={msg}' )
        
    def parse_subprocess( self, response, keyword ):
        '''
        Parse and return the line
        '''
        for line in response.decode("utf-8").split('\n'):
            if keyword in line:
                return line

    def get_balance( self ):
        '''
        Obtain the IDEP balance
        '''
        proc = Popen([ f"iond q bank balances {self.wallet_key}" ], stdout=PIPE, shell=True)
        (out, err) = proc.communicate()
        line = self.parse_subprocess( out, 'amount' )
        balance = line.split('"')[1]
        return balance

    def distribute_rewards( self ):
        '''
        Distribute the rewards from the validator and return the hash
        '''
        child = pexpect.spawn(f"iond tx distribution withdraw-rewards { self.validator_key } --chain-id={ self.chain_id } --from {self.wallet_name} -y", timeout=10)
        child.expect( b'Enter keyring passphrase:' ) 
        child.sendline( self.password )   
        child.expect( pexpect.EOF )                                                                                                                                     
        child.close()
        line = self.parse_subprocess( child.before, 'txhash:' )
        txhash = line.split('txhash: ')[1]
        return txhash

    def distribute_rewards_commission( self ):
        '''
        Distribute the comission for the validator and return the hash
        '''
        child = pexpect.spawn(f"iond tx distribution withdraw-rewards { self.validator_key } --chain-id={ self.chain_id } --from {self.wallet_name} --commission -y", timeout=10)
        child.expect( b'Enter keyring passphrase:' ) 
        child.sendline( self.password )   
        child.expect( pexpect.EOF )                                                                                                                                     
        child.close()
        line = self.parse_subprocess( child.before, 'txhash:' )
        txhash = line.split('txhash: ')[1]
        return txhash

    def delegate( self, amount ):
        '''
        Distribute the rewards from the validator
        '''
        child = pexpect.spawn( f'iond tx staking delegate { self.validator_key } { amount }idep --from { self.wallet_name } --chain-id { self.chain_id } -y', timeout=10)
        child.expect( b'Enter keyring passphrase:' ) 
        child.sendline( self.password )   
        child.expect( pexpect.EOF )                                                                                                                                     
        child.close()
        line = self.parse_subprocess( child.before, 'txhash:' )
        txhash = line.split('txhash: ')[1]
        return txhash
    
    def get_delegations( self ):
        '''
        Obtain the delegation amount for the validator
        '''
        proc = Popen([ f"iond q staking delegations-to  {self.validator_key} --chain-id={self.chain_id}" ], stdout=PIPE, shell=True)
        (out, err) = proc.communicate()
        line = self.parse_subprocess( out, 'shares' )
        balance = line.split('"')[1].split(".")[0]
        return balance

    def delegation_cycle( self ):
        '''
        Delegation cycle for distributing rewards and sending them out
        '''
        self.send( f"{self.name}: Start Delegation Cycle!" )
        self.send( f"{self.name}: Current Delegation: { self.get_delegations() } " )

        self.send( f"{self.name}: Distribution Tx Hash: { self.distribute_rewards() }" )
        time.sleep( 10 )

        self.send( f"{self.name}: Commission Tx Hash: { self.distribute_rewards_commission() }" )
        time.sleep( 10 )
        
        balance = self.get_balance()
        self.send( f"{self.name}: Current Balance (post distribution): { balance } " )
        self.send( f"{self.name}: Delegation Tx Hash: { self.delegate( balance ) }" )
        time.sleep( 10 )

        self.send( f"{self.name}: New Delegation Shares: { self.get_delegations() } " )

idep_bot = IdepAutodelegation()

while True:
    idep_bot.delegation_cycle()
    time.sleep( 3600 )