from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Query

from .extensions import db


class BaseDao:
    def __init__(self, model_cls, db=db):
        self._model = model_cls
        self.db = db

    @property
    def _query(self):
        return self.db.session.query(self._model)

    def get(self, **kwargs):
        return self._query.filter_by(**kwargs).first()

    def one(self, **kwargs):
        return self._query.filter_by(**kwargs).one()

    def create(self, commit=True, **kwargs):
        entity = self._model(**kwargs)
        return self.save(entity, commit=commit)

    def get_or_create(self, **kwargs):
        entity = self.get(**kwargs)
        if not entity:
            entity = self.create(**kwargs)
        return entity

    def update(self, entity, commit=True):
        self.save(entity, commit=commit)

    def delete(self, entity, commit=True):
        self.db.session.delete(entity)
        return commit and self._commit()

    def save(self, entity, commit=True):
        self.db.session.add(entity)
        if commit:
            self._commit()
        return entity

    def _commit(self):
        try:
            self.db.session.commit()
        except SQLAlchemyError:
            self.db.session.rollback()
            raise

    def count(self):
        return self._query.count()

    def all(self) -> Query:
        return self._query

    def get_by_ids(self, ids):
        return self._query.filter(self._model.id.in_(ids))
