

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
    
def set_llm_value(name, decrypt=False, env=ENV):
    '''
    Returns a value for the LLM API from the environment or parameter store.

    Parameters
    ----------
    name : str
        The name of the value to retrieve.
    decrypt : bool
        Whether to decrypt the value.
    env : str
        The environment to retrieve the value from.
    '''

    # get the llm provider
    provider = set_value('LLM_PROVIDER', decrypt=decrypt, env=env)

    # format the value name
    return set_value(f'{provider}_{name}', decrypt=decrypt, env=env)
    

## set configuration

django = {
    'secret_key': set_value('DJANGO_SECRET_KEY', decrypt=True),
}

database = {
    'name': set_value('DB_NAME', decrypt=True),
    'user': set_value('DB_USER', decrypt=True),
    'password': set_value('DB_PASSWORD', decrypt=True),
    'endpoint': set_value('DB_ENDPOINT', decrypt=True),
    'port': set_value('DB_PORT', decrypt=True)
}

llm = {
    'provider': set_value('LLM_PROVIDER'),
    'api_key': set_llm_value('API_KEY', decrypt=True),
    'model': set_llm_value('MODEL'),
    'prompts_path': set_value('PROMPTS_PATH', env='ALL'),
}