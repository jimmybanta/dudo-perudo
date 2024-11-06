''' Contains functions for prompting the LLM API. '''

import logging
import os

import google.generativeai as genai
import typing_extensions as typing

import config
from games.utils import format_bid, format_message_history, load_yaml
from perudo.logic.calculate_probs import calculate_prob

logger = logging.getLogger(__name__)


# get the llm provider
PROVIDER = config.llm['provider']

# load in the pre-written prompts, specific to the provider
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
            round_loser=None,
            bid_probability=None,
            total_dice=None,
            sides_per_die=None
           ):
    ''' 
    Prompts the LLM API with a message.

    Parameters
    ----------
    message_history : list | []
        A list of messages that have been sent in the game.
    round_history : list | []
        A list of the history of the round.
    user_message : str | ''
        The message that the user has sent.
    context : str | None
        The context in which the message is being prompted.
    table : list | []
        A list of the players at the table.
    player : str | None
        The player who is the user.
    stream : bool | True
        Whether to stream the response.
    starting_player : str | None
        The starting player of the game.
    palifico : bool | False
        Whether the game is using palifico rules.
    player_out : str | None
        The player who is out of the game.
    round_total : int | None
        The total number of dice of the called value in the round.
    round_loser : str | None
        The player who lost the round.
    bid_probability : float | None
        The probability of the bid being correct.
    total_dice : int | None
        The total number of dice in the game.
    sides_per_die : int | None
        The number of sides on each die.
    '''

    ## generate system prompt
    # the main prompt is always added to the system
    system_prompt = PROMPTS['main']

    # add in character prompts
    system_prompt += 'The following are the characters in the game: \n'
    if table:
        for character in table:
            if character == player:
                system_prompt += f'The user is {player}. Remember - you should never output a message by the user.\n'
            else:
                base_character = character.split('-')[0]
                system_prompt += f'{character}: {PROMPTS[base_character]} \n'

    ## get the main message
    main_message = ''

    ## add in the context
    # the start of a game
    if context == 'initialize_game':
        main_message = PROMPTS['initialize_game']
        main_message += f'The starting player is: {starting_player}'
    
    # a player made a move
    elif context == 'move':

        # get the player and their move
        move_player = round_history[-1][0]
        move = round_history[-1][1]

        # if it was a bid
        if move != 'call':

            main_message += PROMPTS['move_bid']

            # get the bid
            move = format_bid(move[0], move[1], singular=(move[0] == 1), palifico=palifico)

            next_player = table[(table.index(move_player) + 1) % len(table)]

            main_message += f'{move_player} made the following move: {move}. The player to go next is {next_player}.'

            # add in probability info 
            if bid_probability is not None:
                if bid_probability > 0.75:
                    main_message += f'This is a high probability bid - around {bid_probability * 100:.2f}%.'
                elif bid_probability < 0.25:
                    main_message += f'This is a low probability bid - around {bid_probability * 100:.2f}%.'

        # if it was a call
        else:

            main_message += PROMPTS['move_call']

            # get the bid that they're calling
            last_bid = round_history[-2][1]

            # calculate the probability of this bid
            last_bid_prob = calculate_prob(last_bid, total_dice, palifico=palifico, sides_per_die=sides_per_die)

            main_message += f'''{move_player} called a bid of {format_bid(last_bid[0], last_bid[1], singular=(last_bid[0] == 1), palifico=palifico)}. 
The probability of them being right is around {(1 - last_bid_prob) * 100:.2f}%.'''
            

    # the end of a round
    elif context == 'end_round':

        main_message += PROMPTS['end_round']

        # get the last bid, and the player
        bidding_player, bid = round_history[-2]
        formatted_bid = format_bid(bid[0], bid[1], singular=(bid[0] == 1), palifico=palifico)
        # get the player who called it
        calling_player = round_history[-1][0]

        main_message += f'{bidding_player} made the following bid: {formatted_bid} \n'
        main_message += f'{calling_player} called the bid. \n'
        main_message += f'{round_loser} was wrong - there were {round_total} {bid[1]}s.'

    # a player is out of the game
    elif context == 'player_out':

        main_message += PROMPTS['player_out']
        main_message += f'{player_out} is out of the game.'
        
    # the user has sent a message
    elif context == 'user_message':
        main_message += 'Here is the message history thus far in the game: \n'
        main_message += format_message_history(message_history)

        main_message += PROMPTS['user_message']
        main_message += f'Here is the message: "{user_message}"'


    logger.info(f'Prompting LLM in context={context}')
        
    # if we're prompting from google
    if PROVIDER == 'GOOGLE':

        # configure the API
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
    '''
    Streams the response from the model.
    
    Parameters
    ----------
    model : generativeai.GenerativeModel
        The model to generate the content.
    data : str
        The data to generate the content from.
    generation_config : dict
        The configuration for the generation.
    '''

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


