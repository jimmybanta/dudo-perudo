

def input_int(prompt):
    '''Takes an input and returns an integer. If the input is not an integer, it asks again.'''
    while True:
        try:
            return int(input(prompt))
        except:
            print('Please enter an integer.')