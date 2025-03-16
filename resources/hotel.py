from flask_restful import Resource, reqparse
from models.hotel import HotelModel

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

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('name')
    argumentos.add_argument('stars')
    argumentos.add_argument('daily')
    argumentos.add_argument('city')


    def _find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return


    def get(self, hotel_id):
        hotel = Hotel._find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404


    def post(self, hotel_id):
        hotel = Hotel._find_hotel(hotel_id)
        if hotel:
            return {'message': 'Hotel already exists'}, 409

        dados = Hotel.argumentos.parse_args()
        hotel_obj = HotelModel(hotel_id, **dados)
        new_hotel = hotel_obj.json()
        hoteis.append(new_hotel)

        return new_hotel, 200 
    

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_obj = HotelModel(hotel_id, **dados)
        new_hotel = hotel_obj.json()

        hotel = Hotel._find_hotel(hotel_id)
        if hotel:
            hotel.update(new_hotel)
            return new_hotel, 200
        
        hoteis.append(new_hotel)
        return new_hotel, 201


    def delete(self, hotel_id):
        hotel = Hotel._find_hotel(hotel_id)
        if hotel:
            id = hotel['hotel_id']
            global hoteis
            hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
            return {'message': f'Hotel with id {id} successfully deleted!'}, 200
        
        return {'message': 'Hotel does not exist'}, 400