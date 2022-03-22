from click import argument
from flask_restful import Resource, reqparse
from models.planta import PlantaModel

plantas = [
        {
            'plantaId': 'palmeira',
            'nome': 'Palmeira',
            'ambiente': 'externo',
            'tipoSolo': 'argiloso',
            'porte': 'Pequena',
            'fruto': 'sim'
        },
        {
            'plantaId': 'rosa',
            'nome': 'Rosa',
            'ambiente': 'externo',
            'tipoSolo': 'arenoso',
            'porte': 'Média',
            'fruto': 'sim'
        },
            {
            'plantaId': 'girassol',
            'nome': 'Girassol',
            'ambiente': 'externo',
            'tipoSolo': 'argiloso-arenoso',
            'porte': 'Grande',
            'fruto': 'sim'
        }
]

class Plantas(Resource):
    def get(self):
        return {'plantas': plantas}

class Planta(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('ambiente')
    argumentos.add_argument('tipoSolo')
    argumentos.add_argument('porte')
    argumentos.add_argument('fruto')

    def find_planta(plantaId):

        for planta in plantas :
            if planta['plantaId'] == plantaId:
                return planta
        return None

    def get(self, plantaId):

        planta = Planta.find_planta(plantaId)
        if planta:
            return planta
        return {'message': 'Planta not found.'}, 404

    def post(self, plantaId):
        
        dados = Planta.argumentos.parse_args()
        planta_objeto = PlantaModel(plantaId, ** dados)
        nova_planta = planta_objeto.json()

        plantas.append(nova_planta)
        return nova_planta, 200

    def put(self, plantaId):

        dados = Planta.argumentos.parse_args()
        planta_objeto = PlantaModel(plantaId, ** dados)
        nova_planta = planta_objeto.json()

        planta = Planta.find_planta(plantaId)
        if planta:
            planta.update(nova_planta)
            return nova_planta, 200
        plantas.append(nova_planta)
        return nova_planta, 201      

    def delete(self, plantaId):
        global plantas
        plantas = [planta for planta in plantas if planta['plantaId'] != plantaId]
        return {'message': 'Planta deleted.'}