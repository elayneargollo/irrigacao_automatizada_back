from sql_alchemy import banco

class PlantaModel(banco.Model):
    __tablename__ = 'plantas'

    plantaId = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(150), nullable=False)
    ambiente = banco.Column(banco.String(150), nullable=False)
    tipoSolo = banco.Column(banco.String(50), nullable=False)
    porte = banco.Column(banco.String(30), nullable=False)
    fruto = banco.Column(banco.String(3), nullable=False)

    def __init__(self, plantaId, nome, ambiente, tipoSolo, porte, fruto):
        self.plantaId = plantaId
        self.nome = nome
        self.ambiente = ambiente
        self.tipoSolo = tipoSolo
        self.porte = porte
        self.fruto = fruto

    def json(self):
        return {
            'plantaId': self.plantaId,
            'nome': self.nome,
            'ambiente': self.ambiente,
            'tipoSolo': self.tipoSolo,
            'porte': self.porte,
            'fruto': self.fruto
        }

    def save_planta(self):
        banco.session.add(self)
        banco.session.commit()

    def update_planta(self, nome, ambiente, tipoSolo, porte, fruto):
        self.nome = nome
        self.ambiente = ambiente
        self.tipoSolo = tipoSolo
        self.porte = porte
        self.fruto = fruto

    def delete_planta(self):
        banco.session.delete(self)
        banco.session.commit()

    @classmethod
    def find_planta(cls, plantaId):
        planta = cls.query.filter_by(plantaId=plantaId).first()
        if planta:
            return planta
        return None