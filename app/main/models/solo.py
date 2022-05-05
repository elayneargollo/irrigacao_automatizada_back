from database.sql_alchemy import banco

class SoloModel(banco.Model):
    __tablename__ = 'solos'

    soloId = banco.Column(banco.Integer, primary_key=True)
    tipoSolo = banco.Column(banco.String(150), nullable=False)
    identificador = banco.Column(banco.String(150), nullable=False, unique=True)
    pesoSoloSeco = banco.Column(banco.Float, nullable=True)
    pesoSoloUmido = banco.Column(banco.Float, nullable=True)
    quantidadeAmostra = banco.Column(banco.Integer, nullable=True)

    def __init__(self, tipoSolo, identificador, pesoSoloSeco, pesoSoloUmido, quantidadeAmostra):
        self.tipoSolo = tipoSolo
        self.identificador = identificador
        self.pesoSoloSeco = pesoSoloSeco
        self.pesoSoloUmido = pesoSoloUmido
        self.quantidadeAmostra = quantidadeAmostra
    
    def json(self):
        return {
            'soloId': self.soloId,
            'tipoSolo': self.tipoSolo,
            'identificador': self.identificador,
            'pesoSoloSeco': self.pesoSoloSeco,
            'pesoSoloUmido': self.pesoSoloUmido,
            'quantidadeAmostra': self.quantidadeAmostra
        }

    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    @classmethod
    def find_solo(cls, soloId):
        solo = cls.query.filter_by(soloId=soloId).first()
        if solo:
            return solo
        return None

    @classmethod
    def find_by_tipo(cls, tipoSolo):
        solo = cls.query.filter_by(tipoSolo=tipoSolo).first()
        if solo:
            return solo
        return None