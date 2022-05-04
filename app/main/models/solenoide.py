from database.sql_alchemy import banco
import datetime

class SolenoideModel(banco.Model):
    __tablename__ = 'solenoides'

    solenoideId = banco.Column(banco.Integer, primary_key=True)
    tag = banco.Column(banco.String(150), nullable=True)
    status = banco.Column(banco.String(150), nullable=True)
    dataLeitura = banco.Column(banco.DateTime, default=datetime.datetime.now)
    voltagem = banco.Column(banco.Integer)
    quantidadeVias = banco.Column(banco.Integer)
    corpo = banco.Column(banco.String(150), nullable=True)

    def __init__(self, tag, status, dataLeitura, voltagem, quantidadeVias, corpo):
        self.tag = tag
        self.status = status
        self.dataLeitura = dataLeitura
        self.voltagem = voltagem
        self.quantidadeVias = quantidadeVias
        self.corpo = corpo
    
    def json(self):
        return {
            'solenoideId': self.solenoideId,
            'tag': self.tag,
            'status': self.status,
            'dataLeitura': self.dataLeitura.isoformat(),
            'voltagem': self.voltagem,
            'quantidadeVias': self.quantidadeVias,
            'corpo': self.corpo,
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