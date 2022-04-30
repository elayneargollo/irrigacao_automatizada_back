from database.sql_alchemy import banco

class AmbienteModel(banco.Model):
    __tablename__ = 'ambientes'

    ambienteId = banco.Column(banco.Integer, primary_key=True)
    tipoAmbiente = banco.Column(banco.String(150), nullable=False)
    identificador = banco.Column(banco.String(150), nullable=False)

    def __init__(self, tipoAmbiente, identificador):
        self.tipoAmbiente = tipoAmbiente
        self.identificador = identificador
    
    def json(self):
        return {
            'ambienteId': self.ambienteId,
            'tipoAmbiente': self.tipoAmbiente,
            'identificador': self.identificador,
        }

    def save_ambiente(self):
        banco.session.add(self)
        banco.session.commit()

    @classmethod
    def find_ambiente(cls, ambienteId):
        ambiente = cls.query.filter_by(ambienteId=ambienteId).first()
        if ambiente:
            return ambiente
        return None

    @classmethod
    def find_by_tipo(cls, tipoAmbiente):
        ambiente = cls.query.filter_by(tipoAmbiente=tipoAmbiente).first()
        if ambiente:
            return ambiente
        return None