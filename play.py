from game import Game
import data_service

basic_resources = {'wood': 1200, 'worker': 20}


def start_game(username):
    print('Welcome {}!'.format(username))
    if not data_service.user_exists(username):
        data_service.create_user(username, basic_resources)
    game1 = Game(username)
    command_map = {'st': game1.status_update,
                   'mw': lambda: game1.build_building('woodhouse'),
                   'ew': game1.empty_all}
    while True:
        command = input('--> ')
        if command == 'qq':
            break
        elif command in command_map:
            command_map[command]()
        else:
            print('Unknown command! Try again.')

print('What is your username?')
username = input('--> ')
start_game(username)
