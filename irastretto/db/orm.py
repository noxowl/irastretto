""":mod:'irastretto.db.orm'

"""
from quart import g
from celery import current_task
from sqlalchemy import literal
from sqlalchemy.orm import sessionmaker, session as sqlalchemy_session
from flask_sqlalchemy import declarative_base


class IrastrettoSession(sqlalchemy_session.Session):
    def __import_models(self):
        from irastretto.models.entity import Entity

    def is_exist(self, data_id) -> bool:
        self.__import_models()
        # noinspection PyUnresolvedReferences
        q = self.query(Entity).filter_by(data_id=data_id)
        return self.query(literal(True)).filter(q.exists()).scalar()

    def get_metadata(self, entity_id):
        self.__import_models()
        # noinspection PyUnresolvedReferences
        return self.query(Entity).filter_by(entity_id=entity_id).one_or_none()

    def store_metadata(self, author: str,
                       data_id: str,
                       source: str,
                       description: str) -> object:
        self.__import_models()
        with self.begin():
            # noinspection PyUnresolvedReferences
            entity = Entity(
                data_id=data_id,
                platform=platform,
                author=author,
                source=source,
                description=description)
            self.add(entity)
        return entity

    def store_media(self, media: bytes):
        if 'file://' in g.config['STORAGE']['endpoint']:
            self.__local_storage(media)
        else:
            self.__external_storage(media)

    def __local_storage(self, media):
        pass

    def __external_storage(self, media):
        pass


Base = declarative_base()
Session = sessionmaker(autocommit=True, class_=IrastrettoSession)


def init_database(engine):
    import_all_modules()
    Base.metadata.create_all(engine)


def import_all_modules():
    import irastretto.db.db
