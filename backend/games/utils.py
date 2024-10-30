''' Contains utility functions for the games app. '''

import os
import yaml
import logging

logger = logging.getLogger(__name__)


def load_yaml(file):
    ''' Loads a local yaml file. 
    
    Parameters
    ----------
    file : str
        The path to the yaml file.
        
    Returns
    -------
    dict
        The yaml file as a dictionary.
    '''

    with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data

def format_message_history(message_history):

    final_str = ''

    for message in message_history:

        try:
            final_str += f'[{message["writer"]}]: {message["text"]}\n'
        except:
            logger.exception(f'Error formatting message: {message}')
            continue
    
    return final_str


def format_bid(quantity, value, singular=False, palifico=False):
    '''
    Formats a tuple move into a readable string.
    '''

    value_dict = {
        1: (('one' if singular else 'ones') if palifico else ('jessie' if singular else 'jessies')),
        2: 'two' if singular else 'twos',
        3: 'three' if singular else 'threes',
        4: 'four' if singular else 'fours',
        5: 'five' if singular else 'fives',
        6: 'six' if singular else 'sixes',
    }

    return f'{quantity} {value_dict[value]}'