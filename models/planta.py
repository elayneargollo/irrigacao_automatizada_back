class PlantaModel:
    def __init__(self, plantaId, nome, ambiente, tipoSolo, porte, fruto):
        self.hotelId = plantaId
        self.nome = nome
        self.ambiente = ambiente
        self.tipoSolo = tipoSolo
        self.porte = porte
        self.fruto = fruto

    def json(self):
        return {
            'plantaId': self.hotelId,
            'nome': self.nome,
            'ambiente': self.ambiente,
            'tipoSolo': self.tipoSolo,
            'porte': self.porte,
            'fruto': self.fruto
        }