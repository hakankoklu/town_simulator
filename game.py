from buildings import WoodHouse


building_map = {'woodhouse': WoodHouse}


class Game:

    def __init__(self, username):
        self.username = username
        game_specs = data_service.get_game_specs(username)
        self.resources = game_specs['resources']
        self.buildings = []

    def load_buildings(self):
        building_specs = data_service.get_building_specs(self.username)
        for building_spec in building_specs:
            self.buildings.append(self.load_building(building_spec))

    @staticmethod
    def load_building(building_spec):
        building_type = building_spec.pop('type')
        return building_map[building_type](**building_spec)

    def build_building(self, building_type):
        building_class = building_map[building_type]
        if self.has_resources(building_type):
            self.update_resources(building_type)
            self.buildings.append(building_class())
        else:
            print('Not enough resources!')

    def has_resources(self, building_type):
        for k, v in building_map[building_type].cost.items():
            if self.resources[k] < v:
                return False
        return True

    def update_resources(self, building_type):
        for k, v in building_map[building_type].cost.items():
            self.resources[k] -= v

    def status_update(self):
        resource_report = get
        wood_in_houses = WoodHouse.total_wood()
        woodhouse_count = len(WoodHouse.wood_houses)
        print('Working workers: {}'.format(str(WoodHouse.min_worker * woodhouse_count)))
        print('Available worker: {}'.format(str(men_number)))
        print('Number of woodhouses: {}'.format(str(woodhouse_count)))
        print('Wood in storage: {}'.format(str(wood)))
        print('Wood ready to be harvested: {}'.format(wood_in_houses))
