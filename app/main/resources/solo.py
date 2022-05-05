from click import argument
from flask_restful import Resource, reqparse
from models.solo import SoloModel
from flask_jwt_extended import jwt_required
import logging

logger = logging.getLogger()

atributos = reqparse.RequestParser()
atributos.add_argument('tipoSolo')
atributos.add_argument('identificador')
atributos.add_argument('pesoSoloSeco', type=float)
atributos.add_argument('pesoSoloUmido', type=float)
atributos.add_argument('quantidadeAmostra', type=int)

class Solo(Resource):

    @jwt_required()
    def get(self, soloId):
        logger.info("Acess getById '{}' in Solo".format(soloId))

        solo = SoloModel.find_solo(soloId)
        if solo:
            return solo.json()
        return {'message': 'Tipo de Solo not found.'}, 404
      

class Solos(Resource):

    @classmethod
    def post(cls):
        logger.info('Acess post in Solos')

        dados = atributos.parse_args()

        if SoloModel.find_by_tipo(dados['tipoSolo']):
            return {"message": "Solo '{}' already exists.".format(dados['tipoSolo'])}, 400

        solo = SoloModel(** dados)

        try:
            solo.save_usuario()
        except Exception as e:
            logger.error('Acess post in Solos {}'.format(e))
            return {"message": "An internal error ocurred trying to save."}, 500

        return {"message": "Solo cread successfully!."}, 201

    @jwt_required()
    def get(self):
        logger.info('Acess getAll in Solos')
        return {'solos': [solo.json() for solo in SoloModel.query.all()]}