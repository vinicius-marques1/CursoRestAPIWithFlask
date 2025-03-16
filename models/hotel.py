from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True)
    name = banco.Column(banco.String(80))
    stars = banco.Column(banco.Float(precision=1))
    daily = banco.Column(banco.Float(precision=2))
    city = banco.Column(banco.String(40))

    def __init__(self, hotel_id, name, stars, daily, city):
        self.hotel_id = hotel_id
        self.name = name
        self.stars = stars
        self.daily = daily
        self.city = city


    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'stars': self.stars,
            'daily': self.daily,
            'city': self.city
        }
    
    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()