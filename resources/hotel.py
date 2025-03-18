from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        "hotel_id": "alpha",
        "name": "Alpha Hotel",
        "stars": 4.3,
        "daily": 420.34,
        "city": "Rio de Janeiro"
    },
    {
        "hotel_id": "bravo",
        "name": "Bravo Hotel",
        "stars": 4,
        "daily": 400,
        "city": "São Paulo"
    },
    {
        "hotel_id": "charlie",
        "name": "Charlie Hotel",
        "stars": 3.8,
        "daily": 380.50,
        "city": "Santa Catarina"
    }
]


class Hoteis(Resource):
    def get(self):
        return {"hoteis": [hotel.json() for hotel in HotelModel.query.all()]}


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


    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {"message": "An error ocurred trying to delete hotel."}, 500
            return {"message": "Hotel deleted"}
        return {"message": "Hotel not found"}, 404