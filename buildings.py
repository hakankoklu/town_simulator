from datetime import datetime


class WoodHouse:

    building_name = 'Woodhouse'
    wood_houses = []
    produces = 'wood'
    cost = {'wood': 500, 'worker': 4}
    wood_per_min = 10
    max_storage = 50

    @classmethod
    def total_wood(cls):
        return sum([wh.check_storage() for wh in WoodHouse.wood_houses])

    @classmethod
    def empty_all(cls):
        for wh in WoodHouse.wood_houses:
            wh.empty()

    def __init__(self, created_at=datetime.utcnow(), last_emptied_at=datetime.utcnow()):
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