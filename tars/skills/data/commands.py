import json

def load_commands():
    '''Load commands from json file'''
    with open('tars/skills/data/commands.json') as commands_data:
        commands = json.load(commands_data)
    return commands['commands']
