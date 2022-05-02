from database.sql_alchemy import banco
import datetime

class SolenoideModel(banco.Model):
    __tablename__ = 'solenoides'

    solenoideId = banco.Column(banco.Integer, primary_key=True)
    tag = banco.Column(banco.String(150), nullable=True)
    status = banco.Column(banco.String(150), nullable=True)
    dataLeitura = banco.Column(banco.DateTime, default=datetime.datetime.now)

    def __init__(self, tag, status, dataLeitura):
        self.tag = tag
        self.status = status
        self.dataLeitura = dataLeitura
    
    def json(self):
        return {
            'solenoideId': self.solenoideId,
            'tag': self.tag,
            'status': self.status,
            'dataLeitura': self.dataLeitura.isoformat()
        }

    def save_solenoide(self):
        banco.session.add(self)
        banco.session.commit()

    @classmethod
    def find_solenoide(cls, solenoideId):
        solenoide = cls.query.filter_by(solenoideId=solenoideId).first()
        if solenoide:
            return solenoide
        return None

    @classmethod
    def find_by_tag(cls, tag):
        solenoide = cls.query.filter_by(tag=tag).first()
        if solenoide:
            return solenoide
        return None