from flask_restful import Resource, reqparse

hoteis = [
    {
        'hotel_id': 'alpha',
        'name': 'Alpha Hotel',
        'stars': 4.3,
        'daily': 420.34,
        'city': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'name': 'Bravo Hotel',
        'stars': 4,
        'daily': 400,
        'city': 'São Paulo'
    },
    {
        'hotel_id': 'charlie',
        'name': 'Charlie Hotel',
        'stars': 3.8,
        'daily': 380.50,
        'city': 'Santa Catarina'
    }
]


class Hoteis(Resource):
    def get(self):
        return hoteis


class Hotel(Resource):
    def get(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):

        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return {'message': 'Hotel already exists'}, 409

        argumentos = reqparse.RequestParser()
        argumentos.add_argument('name')
        argumentos.add_argument('stars')
        argumentos.add_argument('daily')
        argumentos.add_argument('city')

        dados = argumentos.parse_args()

        new_hotel = {
            'hotel_id': hotel_id,
            'name': dados['name'],
            'stars': dados['stars'],
            'daily': dados['daily'],
            'city': dados['city'],
        }
        hoteis.append(new_hotel)

        return new_hotel, 200 