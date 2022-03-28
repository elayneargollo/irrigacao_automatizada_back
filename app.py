from re import template
from telnetlib import AUTHENTICATION
from flask import Flask, jsonify, request
from flask_restful import Api
from resources.planta import Plantas, Planta
from resources.usuario import Usuario, UsuarioRegister, UsuarioLogin, UsuarioLogout, UsuarioConfirmado
from resources.solo import Solo, Solos
from resources.ambiente import Ambiente, Ambientes
from resources.porte import Porte, Portes
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from flask_cors import CORS 
from flask_swagger_ui import get_swaggerui_blueprint
from logging.config import dictConfig
from logly.logging_config import logging_config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_DATABASE_URI_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
dictConfig(logging_config)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': " Swagger Sistema Automatizado"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.before_first_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLOCKLIST

@jwt.revoked_token_loader
def token_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401

api.add_resource(Plantas, '/plantas/')
api.add_resource(Planta, '/plantas/<string:plantaId>')

api.add_resource(Solos, '/solos/')
api.add_resource(Solo, '/solos/<int:soloId>')

api.add_resource(Ambientes, '/ambientes/')
api.add_resource(Ambiente, '/ambientes/<int:ambienteId>')

api.add_resource(Portes, '/portes/')
api.add_resource(Porte, '/portes/<int:porteId>')

api.add_resource(Usuario, '/usuarios/<int:usuarioId>')
api.add_resource(UsuarioRegister, '/cadastro')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioLogout, '/logout')
api.add_resource(UsuarioConfirmado, '/confirmacao/<int:usuarioId>')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)