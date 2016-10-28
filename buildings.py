from datetime import datetime
from time import sleep


men_number = 20
wood = 1200


class WoodHouse:

    wood_house_count = 0
    wood_houses = []
    min_men_per_hour = 4
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

    def __init__(self):
        global men_number, wood
        if men_number >= WoodHouse.min_men_per_hour and wood >= WoodHouse.cost:
            men_number -= WoodHouse.min_men_per_hour
            wood -= WoodHouse.cost
            self.created_at = datetime.utcnow()
            self.last_emptied_at = datetime.utcnow()
            WoodHouse.wood_houses.append(self)
        else:
            raise Exception

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


def create_woodhouse():
    try:
        wh1 = WoodHouse()
        return wh1
    except Exception:
        print('Not enough resources!')

wh1 = create_woodhouse()
wh2 = create_woodhouse()
wh3 = create_woodhouse()

print('Current wood is {}, current wood in houses is {}'.format(str(wood), str(wh1.total_wood())))
sleep(10)
print('Current wood is {}, current wood in houses is {}'.format(str(wood), str(wh1.total_wood())))
sleep(10)
print('Current wood is {}, current wood in houses is {}'.format(str(wood), str(wh1.total_wood())))
wh1.empty_all()
print('Current wood is {}, current wood in houses is {}'.format(str(wood), str(wh1.total_wood())))