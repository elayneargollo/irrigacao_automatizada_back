from models import ambiente
from sql_alchemy import banco

class PlantaModel(banco.Model):
    __tablename__ = 'plantas'

    plantaId = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(150), nullable=False)
    fruto = banco.Column(banco.String(3), nullable=False)

    ambienteId = banco.Column(banco.Integer, banco.ForeignKey('ambientes.ambienteId'), nullable=False)
    tipoSoloId = banco.Column(banco.Integer, banco.ForeignKey('solos.soloId'), nullable=False)
    porteId = banco.Column(banco.Integer, banco.ForeignKey('portes.porteId'), nullable=False)

    tipoSolo = banco.relationship('SoloModel')
    porte = banco.relationship('PorteModel')
    ambiente = banco.relationship('AmbienteModel')

    def __init__(self, plantaId, nome, ambienteId, tipoSoloId, porteId, fruto):
        self.plantaId = plantaId
        self.nome = nome
        self.fruto = fruto
        self.ambienteId = ambienteId
        self.tipoSoloId = tipoSoloId
        self.porteId = porteId

    def json(self):
        return {
            'plantaId': self.plantaId,
            'nome': self.nome,
            'fruto': self.fruto,
            'ambiente': self.ambiente.find_ambiente(self.ambienteId).json(),
            'tipoSolo': self.tipoSolo.find_solo(self.tipoSoloId).json(),
            'porte': self.porte.find_porte(self.porteId).json(),
        }

    def save_planta(self):
        banco.session.add(self)
        banco.session.commit()

    def update_planta(self, nome, ambienteId, tipoSoloId, porteId, fruto):
        self.nome = nome
        self.fruto = fruto
        self.ambienteId = ambienteId
        self.tipoSoloId = tipoSoloId
        self.porteId = porteId
        

    def delete_planta(self):
        banco.session.delete(self)
        banco.session.commit()

    @classmethod
    def find_planta(cls, plantaId):
        planta = cls.query.filter_by(plantaId=plantaId).first()
        if planta:
            return planta
        return None