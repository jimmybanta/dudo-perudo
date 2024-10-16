
''' Contains functions for prompting the LLM API. '''

import logging
import os
import typing_extensions as typing

import google.generativeai as genai

import config

from games.utils import load_yaml


logger = logging.getLogger(__name__)


# get the llm provider
PROVIDER = config.llm['provider']




# load in the pre-written prompts, specific to that provider
PROMPTS = load_yaml(os.path.join(config.llm['prompts_path'], f'{config.llm["provider"].lower()}.yaml'))


def prompt(message, 
           characters=[], 
           stream=True, 
           ):
    ''' 
    Prompts the LLM API with a message.

    Parameters
    ----------
    message : str | list
        The message to prompt with. If a list, then it's a list of dictionaries
        with the writer and text of the message in each. 
        If it's a string, then it's just a message.
    characters : list | []
        The characters currently in the game.
    stream : bool | True
        Whether to stream the prompt.
    '''

    ## generate system prompt
    # the main prompt is always added to the system
    system_prompt = PROMPTS['main']

    """ # add in character prompts
    if characters:
        system_prompt += PROMPTS[character] """
    
    # if we're prompting from google
    if PROVIDER == 'GOOGLE':

        genai.configure(api_key=config.llm['api_key'])

        model = genai.GenerativeModel("gemini-1.5-flash",
                                      system_instruction=system_prompt)
        
        # class specifying output format
        class Message(typing.TypedDict):
            '''A message.
            Contains the writer, the text, and the delay, in ms.'''
            writer: str
            text: str
            delay: int

        generation_config = {
            'response_mime_type': 'application/json',
            'response_schema': list[Message]
        }

        data = [
            {'role': 'model', 'parts':
             [{'text': '[riyaaz]: I have 3 threes'}]
            },
            {'role': 'user', 'parts':
             [{'text': '[jimbo]: I have 4 sixes'}]
            },
            {'role': 'model', 'parts':
             [{'text': '[riyaaz]: no way bro - this is insane.'}]
            },
            {'role': 'model', 'parts':
             [{'text': '[theo]: shut up dude'}]
            },
            {'role': 'model', 'parts':
             [{'text': '[riyaaz]: hey your mom called'}]
            },
            {'role': 'user', 'parts':
             [{'text': '[jimbo]: oh yeah? what\'d she say?'}]
            },
        ]
        
        if stream:
            
            return prompt_stream(model, data, generation_config)
        
        else:
            response = model.generate_content(data,
                                            generation_config=generation_config,
                                            stream=False)
            
            return response.text



def prompt_stream(model, data, generation_config):

    for chunk in model.generate_content(data,
                                        generation_config=generation_config,
                                        stream=True):
        yield chunk.text


