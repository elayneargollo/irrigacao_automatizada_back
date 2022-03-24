from sql_alchemy import banco

class PorteModel(banco.Model):
    __tablename__ = 'portes'

    porteId = banco.Column(banco.Integer, primary_key=True)
    descricao = banco.Column(banco.String(150), nullable=False)
    identificador = banco.Column(banco.String(150), nullable=False)

    def __init__(self, descricao, identificador):
        self.descricao = descricao
        self.identificador = identificador
    
    def json(self):
        return {
            'porteId': self.porteId,
            'descricao': self.descricao,
            'identificador': self.identificador
        }

    def save_porte(self):
        banco.session.add(self)
        banco.session.commit()

    @classmethod
    def find_porte(cls, porteId):
        porte = cls.query.filter_by(porteId=porteId).first()
        if porte:
            return porte
        return None

    @classmethod
    def find_by_identificador(cls, identificador):
        porte = cls.query.filter_by(identificador=identificador).first()
        if porte:
            return porte
        return None