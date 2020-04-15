from backend import db
from datetime import datetime
import backend.models as models


class DBHandler:

    @staticmethod
    def get_by_filters(model, filters):
        return model.query.filter_by(**filters).first()

    @staticmethod
    def get_by_id(model, _id):
        return model.query.get(_id)

    @staticmethod
    def get_all(model):
        return model.query.all()

    @staticmethod
    def add(model):
        db.session.add(model)
        db.session.commit()

    @staticmethod
    def delete(model):
        db.session.delete(model)
        db.session.commit()
    
    @staticmethod
    def update():
        db.session.commit()
