import json
import math
from models.car_coordinates import CarCoordinates
from geopy import distance


class Car:
    def __init__(self, lat: float, long: float, timestamp: float, car_index: int):
        self.__lat = lat
        self.__long = long
        self.__timestamp = timestamp
        self.__car_index = car_index
        self.__position = 0
        self.distance_travelled = 0
        self.curr_speed = 0

    def generate_speed_report(self):
        res = {
          'timestamp': self.__timestamp,
          'carIndex': self.__car_index,
          'type': 'SPEED',
          'value': self.curr_speed
        }
        return json.dumps(res)

    def generate_position_report(self):
        res = {
          'timestamp': self.__timestamp,
          'carIndex': self.__car_index,
          'type': 'POSITION',
          'value': self.__position
        }
        return json.dumps(res)

    def update_car_coordinates(self, car_coordinates:dict):
        if CarCoordinates.validate_car_coordinates(car_coordinates) and \
           car_coordinates.get('carIndex') == self.__car_index:
            # Speed in miles per hour
            time_passed = (car_coordinates.get('timestamp') - self.__timestamp) / 1000  # In seconds
            # Avoiding 0 division
            if time_passed > 0:
                p1 = (self.__lat, self.__long)
                p2 = (car_coordinates.get('location').get('lat'), car_coordinates.get('location').get('long'))
                distance_covered = distance.distance(p1, p2).miles  # In miles
                mph = distance_covered / (time_passed / 3600)
            else:
                distance_covered = 0
                mph = 0

            # TODO: Update the position
            self.distance_travelled = self.distance_travelled + distance_covered
            self.curr_speed = mph
            self.__lat = car_coordinates.get('location').get('lat')
            self.__long = car_coordinates.get('location').get('long')
            self.__timestamp = car_coordinates.get('timestamp')

    def get_car_index(self):
        return self.__car_index

    def get_car_position(self):
        return self.__position

    def set_car_position(self, pos):
        self.__position = pos

    def get_car_timestamp(self):
        return self.__timestamp

    def __str__(self):
        return "Car No: " +\
               str(self.__car_index) + ", Race Position: " + \
               str(self.__position) + " Distance travelled: " + \
               str(self.distance_travelled)
