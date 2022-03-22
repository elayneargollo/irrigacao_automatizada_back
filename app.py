from flask import Flask
from flask_restful import Api
from resources.planta import Plantas, Planta
from flask_cors import CORS 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_DATABASE_URI_TRACK_MODIFICATIONS'] = False
api = Api(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.before_first_request
def cria_banco():
    banco.create_all()

api.add_resource(Plantas, '/plantas/')
api.add_resource(Planta, '/plantas/<string:plantaId>')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)