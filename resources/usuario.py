from click import argument
from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blocklist import BLOCKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('nome')
atributos.add_argument('sobrenome')
atributos.add_argument('email', type=str, required=True, help="The field 'email' cannot be left blank")
atributos.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank")

class Usuario(Resource):
    
    @jwt_required()
    def get(self, usuarioId):

        usuario = UsuarioModel.find_usuario(usuarioId)
        if usuario:
            return usuario.json()
        return {'message': 'Usuário not found.'}, 404

class UsuarioRegister(Resource):

    def post(self):
        dados = atributos.parse_args()

        if UsuarioModel.find_by_email(dados['email']):
            return {"message": "E-mail '{}' already exists.".format(dados['email'])}, 400

        usuario = UsuarioModel(** dados)

        try:
            usuario.save_usuario()
        except:
            return {"message": "An internal error ocurred trying to save."}, 500

        return {"message": "User cread successfully!."}, 201

class UsuarioLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        usuario = UsuarioModel.find_by_email(dados['email'])

        if usuario and safe_str_cmp(usuario.password, dados['password']):
            tokenAcesso = create_access_token(identity=usuario.usuarioId)
            return {'access_token': tokenAcesso}, 200
        return {'message': 'The e-mail or password is incorrect.'}, 401
 
class UsuarioLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()["jti"]
        BLOCKLIST.add(jwt_id)
        return {'message': 'Logged out successfully.'}, 200
 

