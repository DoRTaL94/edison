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

    @staticmethod
    def add_blacklisted_jti(jti):
        blacklisted_token = models.Token(jti, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        db.session.add(blacklisted_token)
        db.session.commit()

    @staticmethod
    def is_jti_blacklisted(jti):
        return models.Token.query.get(jti) is not None
