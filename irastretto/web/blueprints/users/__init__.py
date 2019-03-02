""":mod:'irastretto.web.blueprints.users'

"""
from quart import g, request
from quart_openapi import PintBlueprint, Resource

blueprint = PintBlueprint('users', __name__)


@blueprint.route('/users/<user_id>')
class User(Resource):
    async def get(self, user_id):
        return user_id
