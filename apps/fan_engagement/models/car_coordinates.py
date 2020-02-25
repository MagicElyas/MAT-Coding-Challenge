class CarCoordinates:

    @staticmethod
    def validate_car_coordinates(car_status:dict):
        if 'timestamp' in car_status and 'carIndex' in car_status and 'location' in car_status \
                and 'long' in car_status.get('location') and 'lat' in car_status.get('location'):
            return True
        else:
            return False
