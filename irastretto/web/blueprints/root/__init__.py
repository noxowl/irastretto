""":mod:'irastretto.web.blueprints.root'

"""

from quart import g, request, render_template, jsonify
from quart_openapi import PintBlueprint, Resource

from irastretto.services import info

blueprint = PintBlueprint('root', __name__,
                          template_folder='templates'
                          )


@blueprint.route('/')
class Root(Resource):
    async def get(self):
        return await render_template('index.html')


@blueprint.route('/about')
class About(Resource):
    async def get(self):
        return await render_template('about.html')


@blueprint.route('/info')
class Info(Resource):
    async def get(self):
        result = info()
        return jsonify(result)
