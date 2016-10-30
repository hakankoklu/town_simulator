from game import Game
from buildings import WoodHouse


def start_game(username):
    print('Welcome {}!'.format(username))
    game1 = Game(username)
    while True:
        command = input('--> ')
        if command == 'qq':
            break
        elif command in command_map:
            command_map[command]()
        else:
            print('Unknown command! Try again.')

command_map = {'status': status_update,
               'make_wh': create_woodhouse,
               'empty_houses': WoodHouse.empty_all}

print('What is your username?')
username = input('--> ')
start_game(username)
