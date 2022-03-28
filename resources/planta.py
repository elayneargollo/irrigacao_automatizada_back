from click import argument
from flask_restful import Resource, reqparse
from models.planta import PlantaModel
from flask_jwt_extended import jwt_required
import logging

logger = logging.getLogger()

class Plantas(Resource):

    @jwt_required()
    def post(self):
        logger.info('Acess post in Plantas')

        dados = Planta.argumentos.parse_args()
        planta = PlantaModel(** dados)

        try:
            planta.save_planta()
        except Exception as e:
            logger.error('Acess post in Plantas {}'.format(e))
            return {"message": "An internal error ocurred trying to save."}, 500

        return planta.json()

    @jwt_required()
    def get(self):
        logger.info('Acess getAll in Plantas')
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
        logger.info("Acess getById '{}' in Planta".format(plantaId))

        planta = PlantaModel.find_planta(plantaId)
        if planta:
            return planta.json()

        return {'message': 'Planta not found.'}, 404

    @jwt_required()
    def put(self, plantaId):

        logger.info("Acess put '{}' in Planta".format(plantaId))

        dados = Planta.argumentos.parse_args()
        planta_encontrada = PlantaModel.find_planta(plantaId)

        if planta_encontrada:
            planta_encontrada.update_planta(**dados)
            planta_encontrada.save_planta()
            return planta_encontrada.json(), 200
        planta = PlantaModel(plantaId, ** dados)

        try:
            planta.save_planta()
        except Exception as e:
            logger.error('Acess put in Planta {}'.format(e))
            return {"message": "An internal error ocurred trying to save."}, 500

        return planta.json(), 201      

    @jwt_required()
    def delete(self, plantaId):
        
        logger.info("Acess delete '{}' in Planta".format(plantaId))

        planta_encontrada = PlantaModel.find_planta(plantaId)

        if planta_encontrada:
            try:
                planta_encontrada.delete_planta()
            except Exception as e:
                logger.error('Acess delete in Planta {}'.format(e))
                return {"message": "An internal error ocurred trying to delete."}, 500
            return {'message': 'Planta deleted.'}

        return {'message': 'Planta not found.'}, 404