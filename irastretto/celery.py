""":mod:'irastretto.celery'

"""
from celery import Celery, current_app, current_task
from celery.loaders.base import BaseLoader
from celery.signals import celeryd_init, task_failure, task_postrun
from sqlalchemy.engine import Engine, create_engine

from .config import ConfigDict, read_config
from .db.orm import Session


app = Celery(__name__, loader='{0}:Loader'.format(__name__))


class Loader(BaseLoader):
    def read_configuration(self, env='CELERY_CONFIG_MODULE'):
        pass


def get_database_engine() -> Engine:
    config = current_app.conf
    if 'DATABASE_ENGINE' not in config:
        db_url = config['DATABASE_URI']
        config['DATABASE_ENGINE'] = create_engine(db_url)
        if 'CELERY_RESULT_BACKEND' not in config:
            pass
    return config['DATABASE_ENGINE']


def get_session() -> Session:
    task = current_task._get_current_object()
    request = task.request
    if getattr(request, 'db_session', None) is None:
        request.db_session = Session(bind=get_database_engine())
    return request.db_session


@task_postrun.connect
def close_session(task_id, task, *args, **kwargs):
    session = getattr(task.request, 'db_session', None)
    if session is not None:
        session.close()


@celeryd_init.connect
def setup_logging():
    pass


@task_failure.connect
def report_task_failure(task_id, exception, args, kwargs,
                        traceback, einfo, sender):
    pass
