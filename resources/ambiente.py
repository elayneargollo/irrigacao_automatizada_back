from click import argument
from flask_restful import Resource, reqparse
from models.ambiente import AmbienteModel
from flask_jwt_extended import  jwt_required
import logging

logger = logging.getLogger()

atributos = reqparse.RequestParser()
atributos.add_argument('tipoAmbiente')
atributos.add_argument('identificador')

class Ambiente(Resource):

    @jwt_required()
    def get(self, ambienteId):
        logger.info("Acess getById '{}' in Ambiente".format(ambienteId))

        ambiente = AmbienteModel.find_ambiente(ambienteId)
        if ambiente:
            return ambiente.json()
        return {'message': 'Tipo de Ambiente not found.'}, 404
      

class Ambientes(Resource):

    @classmethod
    def post(cls):
        logger.info('Acess post in Ambientes')
        dados = atributos.parse_args()

        if AmbienteModel.find_by_tipo(dados['tipoAmbiente']):
            return {"message": "Ambiente '{}' already exists.".format(dados['tipoAmbiente'])}, 400

        ambiente = AmbienteModel(** dados)

        try:
            ambiente.save_ambiente()
            return {"message": "Ambiente cread successfully!."}, 201
        except Exception as e:
            logger.error('Acess post in Ambientes {}'.format(e))
            return {"message": "An internal error ocurred trying to save."}, 500

    @jwt_required()
    def get(self):
        logger.info('Acess getAll in Ambientes')
        return {'ambientes': [ambiente.json() for ambiente in AmbienteModel.query.all()]}