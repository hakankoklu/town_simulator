from buildings import WoodHouse


building_map = {'woodhouse': WoodHouse}


class Game:

    def __init__(self, username):
        self.username = username
        game_specs = data_service.get_game_specs(username)
        self.worker_count = game_specs['worker_count']
        self.resources = game_specs['resources']
        self.buildings = []

    def load_buildings(self):
        building_specs = data_service.get_building_specs(self.username)
        for building_spec in building_specs:
            self.buildings.append(self.load_building(building_spec))

    @staticmethod
    def load_building(building_spec):
        building_type = building_spec['type']
        return building_map[building_type](**building_spec)

    def build_building(self, building_type):
        building_class = building_map[building_type]
        if self.has_resources(building_type):
            self.update_resources(building_type)
            self.buildings.append(building_class())
        else:
            print('Not enough resources!')