""":mod:'irastretto.web.blueprints.tasks'

"""
from quart import g, request, jsonify
from quart_openapi import PintBlueprint, Resource

from irastretto.services import extractor
from .models import taskVaildator

blueprint = PintBlueprint('tasks', __name__)

TaskValidator = blueprint.create_validator('task_request', taskVaildator)


@blueprint.route('/tasks')
class Tasks(Resource):
    @blueprint.expect(TaskValidator)
    async def post(self) -> dict:
        result = extractor.extract(resource=await request.json)
        return jsonify(result)


@blueprint.route('/tasks/<string:task_id>')
class ExistTasks(Resource):
    async def get(self, task_id):
        return jsonify(task_id)
