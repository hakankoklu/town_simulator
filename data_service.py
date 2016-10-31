from models import get_session
from models import Building, GameUser, Resource

from sqlalchemy import exists, and_


def get_stored_resources(user_id):
    sess = get_session()
    result = {}
    if _check_if_exists(sess, user_id, Resource):
        resources = sess.query(Resource).filter(Resource.user_id == user_id)
        for resource in resources.all():
            result[resource.resource_type] = resource.amount
    sess.close()
    return result


def get_user_id(username):
    sess = get_session()
    user = sess.query(GameUser).filter(GameUser.username == username)
    sess.close()
    if user.count() == 1:
        return user.one().id
    return None


def get_building_specs(user_id):
    sess = get_session()
    result = []
    if _check_if_exists(sess, user_id, Building):
        buildings = sess.query(Building).filter(Building.user_id == user_id)
        for building in buildings.all():
            new_building = {'id': building.id,
                            'building_type': building.building_type,
                            'created_at': building.created_at,
                            'last_harvested': building.last_harvested}
            result.append(new_building)
    sess.close()
    return result


def get_one_building(building_id):
    sess = get_session()
    result = {}
    if sess.query(exists().where(Building.id == building_id)).scalar():
        building = sess.query(Building).filter(Building.id == building_id).one()
        result = {'id': building.id,
                  'created_at': building.created_at,
                  'last_harvested': building.last_harvested}
    sess.close()
    return result


def create_building(user_id, building_type):
    sess = get_session()
    new_building = Building(user_id=user_id, building_type=building_type)
    sess.add(new_building)
    sess.commit()
    result = new_building.id
    sess.close()
    return result


def update_resource(user_id, resource_type, spent):
    sess = get_session()
    resource = sess.query(Resource).filter(and_(Resource.user_id == user_id,
                                                Resource.resource_type == resource_type)).one()
    resource.amount += spent
    sess.commit()
    sess.close()


def user_exists(username):
    return bool(get_user_id(username))


def _check_if_exists(sess, user_id, klass):
    return sess.query(exists().where(klass.user_id == user_id)).scalar()


def create_user(username, basic_resources):
    sess = get_session()
    new_user = GameUser(username=username)
    sess.add(new_user)
    sess.flush()
    for resource, amount in basic_resources.items():
        new_resource = Resource(user_id=new_user.id, resource_type=resource, amount=amount)
        sess.add(new_resource)
    sess.commit()
    sess.close()


def reset_building(building):
    sess = get_session()
    building_to_reset = sess.query(Building).filter(Building.id == building.id).one()
    building_to_reset.last_harvested = building.last_harvested
    sess.commit()
    sess.close()