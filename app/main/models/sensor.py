from database.sql_alchemy import banco
import datetime

class SensorModel(banco.Model):
    __tablename__ = 'sensores'

    sensorId = banco.Column(banco.Integer, primary_key=True)
    tag = banco.Column(banco.String(150), nullable=True)
    nome = banco.Column(banco.String(150), nullable=True)
    status = banco.Column(banco.String(150), nullable=True)
    dataLeitura = banco.Column(banco.DateTime, default=datetime.datetime.now)

    plantaId = banco.Column(banco.Integer, banco.ForeignKey('plantas.plantaId'), nullable=False)
    planta = banco.relationship('PlantaModel')

    solenoideId = banco.Column(banco.Integer, banco.ForeignKey('solenoides.solenoideId'), nullable=False)
    solenoide = banco.relationship('SolenoideModel')

    def __init__(self, tag, nome, status, dataLeitura, solenoideId, plantaId):
        self.tag = tag
        self.nome = nome
        self.status = status
        self.dataLeitura = dataLeitura
        self.solenoideId = solenoideId
        self.plantaId = plantaId
    
    def json(self):
        return {
            'sensorId': self.sensorId,
            'tag': self.tag,
            'nome': self.nome,
            'status': self.status,
            'dataLeitura': self.dataLeitura.isoformat(),
            'solenoide': self.solenoide.find_solenoide(self.solenoideId).json(),
            'planta': self.planta.find_planta(self.plantaId).json()
        }

    def save_sensor(self):
        banco.session.add(self)
        banco.session.commit()

    @classmethod
    def find_sensor(cls, sensorId):
        sensor = cls.query.filter_by(sensorId=sensorId).first()
        if sensor:
            return sensor
        return None

    @classmethod
    def find_by_tag(cls, tag):
        sensor = cls.query.filter_by(tag=tag).first()
        if sensor:
            return sensor
        return None