from click import argument
from flask_restful import Resource, reqparse
from models.solo import SoloModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blocklist import BLOCKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('tipoSolo')
atributos.add_argument('identificador')

class Solo(Resource):

    @jwt_required()
    def get(self, soloId):

        solo = SoloModel.find_solo(soloId)
        if solo:
            return solo.json()
        return {'message': 'Tipo de Solo not found.'}, 404
      

class Solos(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        if SoloModel.find_by_tipo(dados['tipoSolo']):
            return {"message": "Solo '{}' already exists.".format(dados['tipoSolo'])}, 400

        solo = SoloModel(** dados)

        try:
            solo.save_usuario()
        except:
            return {"message": "An internal error ocurred trying to save."}, 500

        return {"message": "Solo cread successfully!."}, 201

    @jwt_required()
    def get(self):
        return {'solos': [solo.json() for solo in SoloModel.query.all()]}