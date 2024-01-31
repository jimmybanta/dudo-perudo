

import json
import os
import dotenv


# load environment variables and aws region
## this is necessary for when celery runs as a daemon
dotenv.load_dotenv()

# set environment
ENV = os.getenv('ENV')


# helper functions
""" def get_parameter(name, decrypt=False, env=ENV):
    '''Returns a parameter from the Parameter store.'''

    # retrieve value from parameter store
    return SSM.get_parameter(Name=f'/{env}/{name}',
                             WithDecryption=decrypt)['Parameter']['Value'] """

def set_value(name, decrypt=False, env=ENV):
    '''Returns a value from the environment or parameter store.'''
    if ENV == 'DEV':
        return os.getenv(name)
    """ elif env in ['STAG', 'PROD', 'ALL']: 
        return get_parameter(name, decrypt=decrypt, env=env)
    else:
        raise ValueError('Invalid environment.') """
    

# use .env file for local development environment
if ENV == 'DEV':
    db_secrets = {
        'username': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }


## set configuration

database = {
    'name': set_value('DB_NAME', decrypt=True),
    'user': db_secrets['username'],
    'password': db_secrets['password'],
    'endpoint': set_value('DB_ENDPOINT', decrypt=True),
    'port': set_value('DB_PORT', decrypt=True)
}