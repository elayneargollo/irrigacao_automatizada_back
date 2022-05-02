from click import argument
from flask_restful import Resource, reqparse
from models.solenoide import SolenoideModel
from flask_jwt_extended import  jwt_required
import logging

logger = logging.getLogger()

atributos = reqparse.RequestParser()
atributos.add_argument('tag')
atributos.add_argument('status')
atributos.add_argument('dataLeitura')

class Solenoide(Resource):

    @jwt_required()
    def get(self, solenoideId):
        logger.info("Acess getById '{}' in Solenoide".format(solenoideId))

        solenoide = SolenoideModel.find_solenoide(solenoideId)
        if solenoide:
            return solenoide.json()
        return {'message': 'Tipo de Solenoide not found.'}, 404
      

class Solenoides(Resource):

    @classmethod
    def post(cls):
        logger.info('Acess post in Solenoides')
       
        dados = atributos.parse_args()
        
        if SolenoideModel.find_by_tag(dados['tag']):
            return {"message": "Solenoide '{}' already exists.".format(dados['tag'])}, 400

        solenoide = SolenoideModel(** dados)

        try:
            solenoide.save_solenoide()
            return {"message": "Solenoide cread successfully!."}, 201
        except Exception as e:
            logger.error('Acess post in Solenoides {}'.format(e))
            return {"message": "An internal error ocurred trying to save."}, 500

    @jwt_required()
    def get(self):
        logger.info('Acess getAll in Solenoides')
        return {'solenoides': [solenoide.json() for solenoide in SolenoideModel.query.all()]}