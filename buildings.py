from datetime import datetime
from config import BUILDING_CONFIG

class Building:

    buildings = []

    @classmethod
    def total_wood(cls):
        return sum([wh.check_storage() for wh in Building.buildings])

    @classmethod
    def empty_all(cls):
        for wh in Building.buildings:
            wh.empty()

    def __init__(self, id, building_type, created_at=datetime.utcnow(),
                 last_harvested=datetime.utcnow()):
        self.id = id
        self.building_type = building_type
        self.properties = BUILDING_CONFIG[building_type]
        self.created_at = created_at
        self.last_harvested = last_harvested
        Building.buildings.append(self)

    @property
    def current_storage(self):
        return int(min(self.properties['max_storage'],
                   self.properties['production_per_min']*(datetime.utcnow() -
                                                          self.last_harvested).seconds/60))

    def empty(self):
        harvest = self.current_storage
        self.last_harvested = datetime.utcnow()
        print('{harvest} {produce} harvested'.format(harvest=str(harvest),
                                                     produce=self.properties['produces']))
        return harvest, self.last_harvested

    def check_storage(self):
        return self.current_storage
