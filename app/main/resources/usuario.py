from email import header
from click import argument
from flask import make_response, render_template
from flask_restful import Resource, reqparse
from importlib_metadata import email
from models.usuario import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from database.blocklist import BLOCKLIST
import logging

logger = logging.getLogger()

atributos = reqparse.RequestParser()
atributos.add_argument('nome', type=str)
atributos.add_argument('sobrenome', type=str)
atributos.add_argument('ativado', type=bool)
atributos.add_argument('email', type=str, required=True, help="The field 'email' cannot be left blank")
atributos.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank")

class Usuario(Resource):
    
    @jwt_required()
    def get(self, usuarioId):
        logger.info("Acess getById '{}' in Usuario".format(usuarioId))

        usuario = UsuarioModel.find_usuario(usuarioId)
        if usuario:
            return usuario.json()
        return {'message': 'Usuário not found.'}, 404

class UsuarioRegister(Resource):

    def post(self):
        logger.info('Acess post in UsuarioRegister')

        dados = atributos.parse_args()

        if not dados.get('email') or dados.get('email') is None:
            return {"message": "The field 'email' cannot be left blank."}, 400

        if UsuarioModel.find_by_email(dados['email']):
            return {"message": "E-mail '{}' already exists.".format(dados['email'])}, 400

        usuario = UsuarioModel(** dados)
        usuario.ativado = False

        try:
            usuario.save_usuario()
            usuario.send_confirmation_email()
        except Exception as e:
            usuario.delete_usuario()
            return {"message": "An internal error ocurred trying to save."}, 500

        return {"message": "User cread successfully!."}, 201

class UsuarioLogin(Resource):

    @classmethod
    def post(cls):
        logger.info('Acess post in UsuarioLogin')

        dados = atributos.parse_args()

        usuario = UsuarioModel.find_by_email(dados['email'])

        if usuario and safe_str_cmp(usuario.password, dados['password']):
            if usuario.ativado:
                tokenAcesso = create_access_token(identity=usuario.usuarioId)
                return {'access_token': tokenAcesso}, 200
            return {'message': 'User not confirmed.'}, 400
        return {'message': 'The e-mail or password is incorrect.'}, 401
 
class UsuarioLogout(Resource):

    @jwt_required()
    def post(self):
        logger.info('Acess post in UsuarioLogout')

        jwt_id = get_jwt()["jti"]
        BLOCKLIST.add(jwt_id)
        return {'message': 'Logged out successfully.'}, 200

class UsuarioConfirmado(Resource):

    @classmethod
    def get(cls, usuarioId):
        logger.info('Acess userconfirmed in UsuarioConfirmado')
        
        usuario = UsuarioModel.find_usuario(usuarioId)

        if not usuario:
            return {"message": "User id '{}' not found.".format(usuarioId)}, 404

        usuario.ativado = True
        usuario.save_usuario()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('usuarioConfirmado.html', email=usuario.email, nome=usuario.nome), 200, headers)
