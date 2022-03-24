from click import argument
from flask_restful import Resource, reqparse
from models.ambiente import AmbienteModel
from flask_jwt_extended import  jwt_required

atributos = reqparse.RequestParser()
atributos.add_argument('tipoAmbiente')
atributos.add_argument('identificador')

class Ambiente(Resource):

    @jwt_required()
    def get(self, ambienteId):

        ambiente = AmbienteModel.find_ambiente(ambienteId)
        if ambiente:
            return ambiente.json()
        return {'message': 'Tipo de Ambiente not found.'}, 404
      

class Ambientes(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        if AmbienteModel.find_by_tipo(dados['tipoAmbiente']):
            return {"message": "Ambiente '{}' already exists.".format(dados['tipoAmbiente'])}, 400

        ambiente = AmbienteModel(** dados)

        try:
            ambiente.save_ambiente()
        except:
            return {"message": "An internal error ocurred trying to save."}, 500

        return {"message": "Ambiente cread successfully!."}, 201

    @jwt_required()
    def get(self):
        return {'ambientes': [ambiente.json() for ambiente in AmbienteModel.query.all()]}