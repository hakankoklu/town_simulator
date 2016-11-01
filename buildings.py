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

    def __init__(self, id, created_at=datetime.utcnow(), last_harvested=datetime.utcnow()):
        self.id = id
        self.created_at = created_at
        self.last_harvested = last_harvested
        WoodHouse.wood_houses.append(self)

    @property
    def current_storage(self):
        return int(min(WoodHouse.max_storage,
                   WoodHouse.wood_per_min*(datetime.utcnow() - self.last_harvested).seconds/60))

    def empty(self):
        harvest = self.current_storage
        self.last_harvested = datetime.utcnow()
        print('{harvest} wood harvested'.format(harvest=str(harvest)))
        return harvest, self.last_harvested

    def check_storage(self):
        return self.current_storage
