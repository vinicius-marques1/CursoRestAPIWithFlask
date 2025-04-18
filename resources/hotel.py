from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
from flask import request
import sqlite3

def normalize_path_params(city = None,
                          stars_max = 5,
                          stars_min = 0,
                          daily_max = 10000,
                          daily_min = 0,
                          limit = 50,
                          offset = 0,
                          **kwargs):
    if city:
        return {
            "city": city,
            "stars_min": stars_min,
            "stars_max": stars_max,
            "daily_min": daily_min,
            "daily_max": daily_max,
            "limit": limit,
            "offset": offset
        }
    return {
        "stars_min": stars_min,
        "stars_max": stars_max,
        "daily_min": daily_min,
        "daily_max": daily_max,
        "limit": limit,
        "offset": offset
    }


path_params = reqparse.RequestParser()
path_params.add_argument('city', type=str)
path_params.add_argument('stars_max', type=float)
path_params.add_argument('stars_mim', type=float)
path_params.add_argument('daily_max', type=float)
path_params.add_argument('daily_min', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        # Conexão com o banco de dados
        conn = sqlite3.connect('instance/banco.db')
        cursor = conn.cursor()

        # dados = path_params.parse_args()
        dados = request.args.to_dict()
        dados_validos = {key: value for key, value in dados.items() if value is not None}
        parametros = normalize_path_params(**dados_validos)

        if parametros.get('city'):
            query = "SELECT * FROM hoteis \
                WHERE city = ? \
                AND stars BETWEEN ? AND ? \
                AND daily BETWEEN ? AND ? \
                LIMIT ? OFFSET ?"
            query_params = tuple([value for value in parametros.values()])
            results = cursor.execute(query, query_params)
        else:
            query = "SELECT * FROM hoteis \
                WHERE stars BETWEEN ? AND ? \
                AND daily BETWEEN ? AND ? \
                LIMIT ? OFFSET ?"
            query_params = tuple([value for value in parametros.values()])
            results = cursor.execute(query, query_params)

        hoteis = []
        for row in results:
            hoteis.append({
                'hotel_id': row[0],
                'name': row[1],
                'stars': row[2],
                'daily': row[3],
                'city': row[4]
            })
        conn.close()

        return {"hoteis": hoteis}, 200


class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('name', type=str, required=True, help="The field 'name' can not be left blank")
    argumentos.add_argument('stars', type=float, required=True, help="The field stars can not be left blank")
    argumentos.add_argument('daily')
    argumentos.add_argument('city')



    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404


    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel id '{hotel_id}' already exists"}, 409

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500
        return hotel.json()
    

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()

        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.update_hotel(**dados)
            try:
                hotel.save_hotel()
            except:
                return {"message": "An internal error ocurred trying to save hotel."}, 500
            return hotel.json(), 200
        
        new_hotel = HotelModel(hotel_id, **dados)
        try:
            new_hotel.save_hotel()
        except Exception as e:
            print(e)
            return {"message": "An internal error ocurred trying to save hotel."}, 500
        return new_hotel.json(), 201


    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {"message": "An error ocurred trying to delete hotel."}, 500
            return {"message": "Hotel deleted"}
        return {"message": "Hotel not found"}, 404