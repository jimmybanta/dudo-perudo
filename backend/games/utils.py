''' Contains utility functions for the games app. '''

import os
import yaml

import config



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

        final_str += f'[{message["writer"]}]: {message["text"]}\n'
    
    return final_str

""" def add_info_to_initialization_prompt(theme, timeframe, details, prompt=''):
    ''' 
    Adds information to an initialization prompt - for use when starting a new game. 

    Parameters
    ----------
    theme : str
        The theme of the game.
    timeframe : str
        The timeframe of the game.
    details : str
        The details of the game.
    prompt : str
        The initial prompt.
    
    Returns
    -------
    str
        The updated prompt.
    '''

    # add theme to the prompt
    prompt += f' The theme is {theme}. ' if theme else 'There is no specified theme. '

    # add timeframe
    prompt += f'The timeframe is {timeframe}. ' if timeframe else 'There is no specified timeframe. '

    # add details
    if details:
        prompt += 'The following details will be incorporated into the scenario: '
        for detail in details.split(','):
            prompt += f'{detail},'
        # remove the trailing comma
        prompt = prompt[:-1]
        # add a period
        prompt += '.'


    return prompt

def get_gamefile_listdir(path):
    ''' 
    Returns the list of files in a game file - either local or from s3, depending on the environment.
    All files should be named with an integer, e.g. 1.json, 2.json, etc. 

    Parameters
    ----------
    path : str
        The path to the directory.
    
    Returns
    -------
    list
        The list of files in the directory/prefix.
    '''

    if config.ENV == 'DEV':
        files = sorted(os.listdir(path))

    else:
        files = list_objects(config.s3['data_bucket'], prefix=path)

    # remove any files that don't end in .json
    files = [file for file in files if file.endswith('.json')]

    # filter out any files that don't start with an integer
    files = [file for file in files if file.split('.')[0].isdigit()]

    return files

def get_file_size(filepath):
    '''
    Returns the size of a file in bytes.
    Loads file locally or from s3, depending on the environment.

    Parameters
    ----------
    filepath : str
        The path to the file.

    Returns
    -------
    int
        The size of the file in bytes.
    '''

    if config.ENV == 'DEV':
        return os.path.getsize(filepath)
    else:
        return len(read_object(config.s3['data_bucket'], filepath))
    
def check_file_exists(filepath):
    '''
    Checks if a file exists.
    Loads file locally or from s3, depending on the environment.

    Parameters
    ----------
    filepath : str
        The path to the file.

    Returns
    -------
    bool
        Whether the file exists.
    '''

    if config.ENV == 'DEV':
        return os.path.exists(filepath)
    else:
        return check_object_exists(config.s3['data_bucket'], filepath)

 """