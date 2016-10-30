from datetime import datetime
from


worker_number = 20
wood = 1200


class WoodHouse:

    wood_houses = []
    min_worker = 4
    cost = 500
    wood_per_min = 10
    max_storage = 50

    @classmethod
    def total_wood(cls):
        return sum([wh.check_storage() for wh in WoodHouse.wood_houses])

    @classmethod
    def empty_all(cls):
        for wh in WoodHouse.wood_houses:
            wh.empty()

    def __init__(self, type=None, created_at=datetime.utcnow(), last_emptied_at=datetime.utcnow()):
        self.created_at = created_at
        self.last_emptied_at = last_emptied_at
        WoodHouse.wood_houses.append(self)

    @property
    def current_storage(self):
        return min(WoodHouse.max_storage,
                   WoodHouse.wood_per_min*(datetime.utcnow() - self.last_emptied_at).seconds/60)

    def empty(self):
        global wood
        harvest = self.current_storage
        self.last_emptied_at = datetime.utcnow()
        wood += harvest
        print('{harvest} wood harvested'.format(harvest=str(harvest)))

    def check_storage(self):
        return self.current_storage


def status_update():
    wood_in_houses = WoodHouse.total_wood()
    woodhouse_count = len(WoodHouse.wood_houses)
    print('Working workers: {}'.format(str(WoodHouse.min_worker * woodhouse_count)))
    print('Available worker: {}'.format(str(men_number)))
    print('Number of woodhouses: {}'.format(str(woodhouse_count)))
    print('Wood in storage: {}'.format(str(wood)))
    print('Wood ready to be harvested: {}'.format(wood_in_houses))


def load_game(username):
    print('Welcome {}!'.format(username))
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
if check_user(username):
    load_game(username)
else:
    new_game()