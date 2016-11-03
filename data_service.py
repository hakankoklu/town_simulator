from models import session_scope
from models import Building, GameUser, Resource

from sqlalchemy import exists, and_


def get_stored_resources(user_id):
    with session_scope() as sess:
        return _get_stored_resources(sess, user_id)


def _get_stored_resources(sess, user_id):
    result = {}
    if _check_if_exists(sess, user_id, Resource):
        resources = sess.query(Resource).filter(Resource.user_id == user_id)
        for resource in resources.all():
            result[resource.resource_type] = resource.amount
    return result


def get_user_id(username):
    with session_scope() as sess:
        return _get_user_id(sess, username)


def _get_user_id(sess, username):
    user = sess.query(GameUser).filter(GameUser.username == username)
    if user.count() == 1:
        return user.one().id
    return None


def get_building_specs(user_id):
    with session_scope() as sess:
        return _get_building_specs(sess, user_id)


def _get_building_specs(sess, user_id):
    result = []
    if _check_if_exists(sess, user_id, Building):
        buildings = sess.query(Building).filter(Building.user_id == user_id)
        for building in buildings.all():
            new_building = {'id': building.id,
                            'building_type': building.building_type,
                            'created_at': building.created_at,
                            'last_harvested': building.last_harvested}
            result.append(new_building)
    return result


def get_one_building(building_id):
    with session_scope() as sess:
        return _get_building_by_id(sess, building_id)


def _get_building_by_id(sess, building_id):
    result = {}
    if sess.query(exists().where(Building.id == building_id)).scalar():
        building = sess.query(Building).filter(Building.id == building_id).one()
        result = {'id': building.id,
                  'building_type': building.building_type,
                  'created_at': building.created_at,
                  'last_harvested': building.last_harvested}
    return result


def build_building_with_resources(user_id, building_type, building_cost):
    with session_scope() as sess:
        building_id = _create_building(sess, user_id, building_type)
        _update_resources_by_cost(sess, user_id, building_cost)
        return building_id


def _create_building(sess, user_id, building_type):
    new_building = Building(user_id=user_id, building_type=building_type)
    sess.add(new_building)
    sess.flush()
    result = new_building.id
    return result


def _update_resources_by_cost(sess, user_id, building_cost):
    for k, v in building_cost.items():
        _update_resource(sess, user_id, k, -1 * v)


def update_resource(user_id, resource_type, update_amount):
    with session_scope() as sess:
        _update_resource(sess, user_id, resource_type, update_amount)


def _update_resource(sess, user_id, resource_type, update_amount):
    resource = sess.query(Resource).filter(and_(Resource.user_id == user_id,
                                                Resource.resource_type == resource_type)).one()
    resource.amount += update_amount


def user_exists(username):
    return bool(get_user_id(username))


def _check_if_exists(sess, user_id, klass):
    return sess.query(exists().where(klass.user_id == user_id)).scalar()


def create_user(sess, username, basic_resources):
    new_user = GameUser(username=username)
    sess.add(new_user)
    sess.flush()
    for resource, amount in basic_resources.items():
        new_resource = Resource(user_id=new_user.id, resource_type=resource, amount=amount)
        sess.add(new_resource)


def _reset_building(sess, building):
    building_to_reset = sess.query(Building).filter(Building.id == building.id).one()
    building_to_reset.last_harvested = building.last_harvested


def empty_building_and_update_resources(user_id, resource_type, amount, building):
    with session_scope() as sess:
        _reset_building(sess, building)
        _update_resource(sess, user_id, resource_type, amount)
