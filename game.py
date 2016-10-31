from buildings import WoodHouse
import data_service


building_map = {'woodhouse': WoodHouse}


class Game:

    def __init__(self, username):
        self.username = username
        self.user_id = data_service.get_user_id(username)
        self.load_resources()
        self.buildings = self.load_buildings()

    def load_buildings(self):
        building_specs = data_service.get_building_specs(self.user_id)
        result = []
        for building_spec in building_specs:
            result.append(self.load_building(building_spec))
        return result

    def load_resources(self):
        self.resources = data_service.get_stored_resources(self.user_id)

    @staticmethod
    def load_building(building_spec):
        building_type = building_spec.pop('building_type')
        return building_map[building_type](**building_spec)

    def build_building(self, building_type):
        building_class = building_map[building_type]
        if self.has_resources(building_type):
            building_id = data_service.create_building(self.user_id, building_type)
            self.update_resources_for_built(building_type)
            new_building_specs = data_service.get_one_building(building_id)
            self.buildings.append(building_class(**new_building_specs))
        else:
            print('Not enough resources!')

    def has_resources(self, building_type):
        for k, v in building_map[building_type].cost.items():
            if self.resources[k] < v:
                return False
        return True

    def update_resources_for_built(self, building_type):
        for k, v in building_map[building_type].cost.items():
            self.update_resources(k, -1*v)

    def update_resources(self, resource_type, amount):
        data_service.update_resource(self.user_id, resource_type, amount)
        self.resources[resource_type] += amount

    def status_update(self):
        resource_report = self.get_resource_report()
        building_report = self.get_building_report()
        print(resource_report)
        print(building_report)

    def empty_all(self):
        for building in self.buildings:
            self.update_resources(building.produces, building.empty())
            data_service.reset_building(building)

    def get_resource_report(self):
        rep = ''
        for resource_type, amount in self.resources.items():
            rep += '{} count: {}\n'.format(resource_type, str(amount))
        return rep

    def get_building_report(self):
        rep = ''
        for building in self.buildings:
            rep += '{} count in building {}: {}\n'.format(building.produces, str(building.id),
                                                          str(building.check_storage()))
        return rep
