from click import argument
from flask_restful import Resource, reqparse
from models.porte import PorteModel
from flask_jwt_extended import jwt_required
import logging

logger = logging.getLogger()

atributos = reqparse.RequestParser()
atributos.add_argument('descricao')
atributos.add_argument('identificador')

class Porte(Resource):

    @jwt_required()
    def get(self, porteId):
        logger.info("Acess getById '{}' in Porte".format(porteId))

        porte = PorteModel.find_porte(porteId)
        if porte:
            return porte.json()
        return {'message': 'Porte not found.'}, 404

class Portes(Resource):

    @jwt_required()
    def get(self):
        logger.info('Acess getAll in Portes')
        return {'portes': [porte.json() for porte in PorteModel.query.all()]}

    @classmethod
    def post(cls):
        logger.info('Acess post in Portes')
        dados = atributos.parse_args()

        if PorteModel.find_by_identificador(dados['identificador']):
            logger.info("Porte '{}' already exists.".format(dados['identificador']))
            return {"message": "Porte '{}' already exists.".format(dados['identificador'])}, 400

        porte = PorteModel(** dados)

        try:
            porte.save_porte()
        except Exception as e:
            logger.error('Acess post in Portes {}'.format(e))
            return {"message": "An internal error ocurred trying to save."}, 500
            
        return {"message": "Porte cread successfully!."}, 201