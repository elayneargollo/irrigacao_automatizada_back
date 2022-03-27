from click import argument
from flask_restful import Resource, reqparse
from models.planta import PlantaModel
from flask_jwt_extended import jwt_required

class Plantas(Resource):
    @jwt_required()
    def get(self):
        return {'plantas': [planta.json() for planta in PlantaModel.query.all()]}

class Planta(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('ambienteId', type=str, required=True, help="The field 'ambienteId' cannot be left blank")
    argumentos.add_argument('tipoSoloId', type=str, required=True, help="The field 'tipoSoloId' cannot be left blank")
    argumentos.add_argument('porteId', type=str, required=True, help="The field 'porteId' cannot be left blank")
    argumentos.add_argument('fruto', type=str, required=True, help="The field 'fruto' cannot be left blank")

    @jwt_required()
    def get(self, plantaId):

        planta = PlantaModel.find_planta(plantaId)
        if planta:
            return planta.json()
        return {'message': 'Planta not found.'}, 404

    @jwt_required()
    def post(self, plantaId):
        if PlantaModel.find_planta(plantaId):
            return {"message": "Planta '{}' already exists.".format(plantaId)}, 400

        dados = Planta.argumentos.parse_args()
        planta = PlantaModel(plantaId, ** dados)

        try:
            planta.save_planta()
        except:
            return {"message": "An internal error ocurred trying to save."}, 500

        return planta.json()

    @jwt_required()
    def put(self, plantaId):

        dados = Planta.argumentos.parse_args()
        planta_encontrada = PlantaModel.find_planta(plantaId)

        if planta_encontrada:
            planta_encontrada.update_planta(**dados)
            planta_encontrada.save_planta()
            return planta_encontrada.json(), 200
        planta = PlantaModel(plantaId, ** dados)

        try:
            planta.save_planta()
        except:
            return {"message": "An internal error ocurred trying to save."}, 500

        return planta.json(), 201      

    @jwt_required()
    def delete(self, plantaId):
        planta_encontrada = PlantaModel.find_planta(plantaId)

        if planta_encontrada:
            try:
                planta_encontrada.delete_planta()
            except:
                return {"message": "An internal error ocurred trying to delete."}, 500
            return {'message': 'Planta deleted.'}
        return {'message': 'Planta not found.'}, 404