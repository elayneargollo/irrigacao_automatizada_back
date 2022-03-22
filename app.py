from flask import Flask
from flask_restful import Api
from resources.planta import Plantas, Planta
from flask_cors import CORS 

app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(Plantas, '/plantas/')
api.add_resource(Planta, '/plantas/<string:plantaId>')

if __name__ == '__main__':
    app.run(debug=True)