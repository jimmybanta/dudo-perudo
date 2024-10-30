
''' Contains functions for prompting the LLM API. '''

import logging
import os
import typing_extensions as typing

import google.generativeai as genai

import config

from games.utils import load_yaml, format_message_history, format_bid


logger = logging.getLogger(__name__)


# get the llm provider
PROVIDER = config.llm['provider']




# load in the pre-written prompts, specific to that provider
PROMPTS = load_yaml(os.path.join(config.llm['prompts_path'], f'{config.llm["provider"].lower()}.yaml'))


def prompt(message_history=[],
            round_history=[],
            user_message='',
            context=None,
            table=[], 
            player=None,
            stream=True, 
            starting_player=None,
            palifico=False,
            player_out=None,
            round_total=None,
            round_loser=None
           ):
    ''' 
    Prompts the LLM API with a message.

    Parameters
    ----------
    message : str | list
        The message to prompt with. If a list, then it's a list of dictionaries
        with the writer and text of the message in each. 
        If it's a string, then it's just a message.
    table : list | []
        The characters currently at the table.
    stream : bool | True
        Whether to stream the prompt.
    '''

    ## generate system prompt
    # the main prompt is always added to the system
    system_prompt = PROMPTS['main']

    system_prompt += 'The following are the characters in the game: \n'

    # add in character prompts
    if table:
        for character in table:
            if character == player:
                system_prompt += f'The user is {player}. Remember - you should never output a message by the user.\n'
            else:
                base_character = character.split('-')[0]
                system_prompt += f'{character}: {PROMPTS[base_character]} \n'

    main_message = ''

    # add in the context
    if context == 'initialize_game':
        main_message = PROMPTS['initialize_game']
        main_message += f'The starting player is: {starting_player}'

        logger.info(f'      The starting player is: {starting_player}')
    
    elif context == 'move':

        move_player = round_history[-1][0]
        move = round_history[-1][1]

        if move != 'call':
            move = format_bid(move[0], move[1], singular=(move[0] == 1), palifico=palifico)

        main_message += 'Here is the message history thus far in the game: \n'
        main_message += format_message_history(message_history)

        main_message += PROMPTS['move']
        main_message += f'{move_player} made the following move: {move}'

        logger.info(f'      {move_player} made the following move: {move}')

    elif context == 'end_round':

        main_message += 'Here is the message history thus far in the game: \n'
        main_message += format_message_history(message_history)

        main_message += PROMPTS['end_round']

        bidding_player, bid = round_history[-2]
        formatted_bid = format_bid(bid[0], bid[1], singular=(bid[0] == 1), palifico=palifico)
        calling_player = round_history[-1][0]

        main_message += f'{bidding_player} made the following bid: {formatted_bid} \n'
        main_message += f'{calling_player} called the bid. \n'
        main_message += f'{round_loser} was wrong - there were {round_total} {bid[1]}s.'

        logger.info(f'      {bidding_player} made the following bid: {formatted_bid}')
        logger.info(f'      {calling_player} called the bid.')
        logger.info(f'      {round_loser} was wrong - there were {format_bid(round_total, bid[1], singular=(round_total == 1), palifico=palifico)}.')

    elif context == 'player_out':

        main_message += 'Here is the message history thus far in the game: \n'
        main_message += format_message_history(message_history)

        main_message += PROMPTS['player_out']
        main_message += f'{player_out} is out of the game.'

        logger.info(f'      {player_out} is out of the game.')
        
    elif context == 'user_message':
        main_message += 'Here is the message history thus far in the game: \n'
        main_message += format_message_history(message_history)

        main_message += PROMPTS['user_message']
        main_message += f'Here is the message: "{user_message}"'

        logger.info(f'      Here is the message: "{user_message}"')
    
    logger.info(f'Prompting LLM in context={context}')
        
    # if we're prompting from google
    if PROVIDER == 'GOOGLE':

        genai.configure(api_key=config.llm['api_key'])

        model = genai.GenerativeModel(config.llm['model'],
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
        
        if stream:
            
            return prompt_stream(model, main_message, generation_config)
        
        else:
            response = model.generate_content(main_message,
                                            generation_config=generation_config,
                                            stream=False,
                                            safety_settings={
                                                'HATE': 'BLOCK_NONE',
                                                'HARASSMENT': 'BLOCK_NONE',
                                                'SEXUAL' : 'BLOCK_NONE',
                                                'DANGEROUS' : 'BLOCK_NONE'
                                            })
            
            return response.text
            



def prompt_stream(model, data, generation_config):

    for chunk in model.generate_content(data,
                                        generation_config=generation_config,
                                        stream=True,
                                        safety_settings={
                                                'HATE': 'BLOCK_NONE',
                                                'HARASSMENT': 'BLOCK_NONE',
                                                'SEXUAL' : 'BLOCK_NONE',
                                                'DANGEROUS' : 'BLOCK_NONE'
                                            }):
        yield chunk.text


