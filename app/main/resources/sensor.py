from click import argument
from flask_restful import Resource, reqparse
from models.sensor import SensorModel
from flask_jwt_extended import jwt_required
import logging

logger = logging.getLogger()

class Sensores(Resource):

    @jwt_required()
    def post(self):
        logger.info('Acess post in Sensores')

        dados = Sensor.argumentos.parse_args()
        sensor = SensorModel(** dados)

        try:
            sensor.save_sensor()
        except Exception as e:
            logger.error('Acess post in Sensores {}'.format(e))
            return {"message": "An internal error ocurred trying to save."}, 500

        return sensor.json()

    @jwt_required()
    def get(self):
        logger.info('Acess getAll in Sensores')
        return {'sensores': [sensor.json() for sensor in SensorModel.query.all()]}

class Sensor(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('tag', type=str, required=True, help="The field 'tag' cannot be left blank")
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('status', type=str, required=True, help="The field 'status' cannot be left blank")
    argumentos.add_argument('dataLeitura')
    argumentos.add_argument('solenoideId', type=str, required=True, help="The field 'solenoideId' cannot be left blank")
    argumentos.add_argument('plantaId', type=str, required=True, help="The field 'plantaId' cannot be left blank")

    @jwt_required()
    def get(self, sensorId):
        logger.info("Acess getById '{}' in Sensor".format(sensorId))

        planta = SensorModel.find_sensor(sensorId)
        if planta:
            return planta.json()

        return {'message': 'Sensor not found.'}, 404

    @jwt_required()
    def put(self, sensorId):

        logger.info("Acess put '{}' in Sensor".format(sensorId))

        dados = Sensor.argumentos.parse_args()
        sensor_encontrada = SensorModel.find_sensor(sensorId)

        if sensor_encontrada:
            sensor_encontrada.update_planta(**dados)
            sensor_encontrada.save_planta()
            return sensor_encontrada.json(), 200
        sensor = SensorModel(sensorId, ** dados)

        try:
            sensor.save_planta()
        except Exception as e:
            logger.error('Acess put in Sensor {}'.format(e))
            return {"message": "An internal error ocurred trying to save."}, 500

        return sensor.json(), 201