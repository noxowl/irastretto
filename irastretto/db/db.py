""":mod:'irastretto.db.db'

"""
import os
from quart import current_app, g, _app_ctx_stack
from quart.local import LocalProxy, LocalStack
from sqlalchemy import create_engine
from .orm import Session


def __assemble_database_uri(config: dict):
    return "{0}{1}{2}@{3}/{4}?{5}".format(
        config['DATABASE_URI'],
        config['DATABASE']['rdbms']['username'],
        config['DATABASE']['rdbms']['password'],
        config['DATABASE']['rdbms']['hostname'],
        config['DATABASE']['rdbms']['database'],
        ''  # database args
    )


def get_database_engine():
    """Get a database engine.

    :returns: a database engine
    :rtype: :class: 'sqlalchemy.engine.base.Engine'
    """
    config = current_app.config
    try:
        return config['DATABASE_ENGINE']
    except KeyError:
        if 'sqlite' in config['DATABASE_URI']:
            engine = '{0}/db/{1}'.format(os.path.dirname(__file__), 'app.db')
        else:
            db_uri = __assemble_database_uri(config)
            engine = create_engine(db_uri, **get_database_options())
        config['DATABASE_ENGINE'] = engine
        return engine


def get_database_options():
    return {
        "convert_unicode": True,
        "encoding": 'utf-8',
        # "echo": True,
        "pool_size": 20,
        "pool_recycle": 28000,
        "max_overflow": 15,
    }


def get_session():
    try:
        app_ctx_session = _app_ctx_stack.session
    except (AttributeError, RuntimeError):
        pass
    else:
        return app_ctx_session
    if hasattr(g, 'session'):
        return g.session
    sess = Session(bind=get_database_engine())
    try:
        g.session = sess
    except RuntimeError:
        pass
    return sess


def close_session(exception=None):
    if hasattr(g, 'session'):
        g.session.close()


def setup_session(app):
    app.teardown_appcontext(close_session)


session = LocalProxy(get_session)
