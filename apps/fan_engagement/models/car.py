import json
import math
from models.car_coordinates import CarCoordinates
from geopy import distance


class Car:
    """Class that represents a car in the circuit.
    A car is represented by
    Latitude
    Longitude
    Timestamp -- Last time that the car was updated with a message
    Car index
    Position -- Position of the car in the race
    Distance travelled -- Calculated using latitude and longitude changes
    Current speed -- Calculated using latitude and longitude changes
    """
    def __init__(self, lat: float, long: float, timestamp: float, car_index: int):
        """ Constructs the Car object """
        self.__lat = lat
        self.__long = long
        self.__timestamp = timestamp
        self.__car_index = car_index
        self.__position = 0
        self.distance_travelled = 0
        self.curr_speed = 0

    def generate_speed_report(self):
        """Generates a dictionary with the speed report and returns the dumped json"""
        res = {
            'timestamp': self.__timestamp,
            'carIndex': self.__car_index,
            'type': 'SPEED',
            'value': self.curr_speed
        }
        return json.dumps(res)

    def generate_position_report(self):
        """Generates a dictionary with the position report and returns the dumped json"""
        res = {
            'timestamp': self.__timestamp,
            'carIndex': self.__car_index,
            'type': 'POSITION',
            'value': self.__position
        }
        return json.dumps(res)

    def update_car_coordinates(self, car_coordinates: dict):
        """Receives a car cordinate dictionary and updates:
           Speed
           Distance
           Latitude
           Longitude
           Timestamp
           """
        if CarCoordinates.validate_car_coordinates(car_coordinates) and \
           car_coordinates.get('carIndex') == self.__car_index:
            # Speed in miles per hour
            time_passed = (car_coordinates.get('timestamp') - self.__timestamp) / 1000  # In seconds
            # Avoiding 0 division
            if time_passed > 0:
                p1 = (self.__lat, self.__long)
                p2 = (car_coordinates.get('location').get('lat'),
                      car_coordinates.get('location').get('long'))
                distance_covered = distance.distance(p1, p2).miles  # In miles
                mph = distance_covered / (time_passed / 3600)
            else:
                distance_covered = 0
                mph = 0

            self.distance_travelled = self.distance_travelled + distance_covered
            self.curr_speed = mph
            self.__lat = car_coordinates.get('location').get('lat')
            self.__long = car_coordinates.get('location').get('long')
            self.__timestamp = car_coordinates.get('timestamp')

    def get_car_index(self):
        """Returns the car index"""
        return self.__car_index

    def get_car_position(self):
        """Returns the car position"""
        return self.__position

    def set_car_position(self, pos):
        """Returns the car position in the race"""
        self.__position = pos

    def get_car_timestamp(self):
        """Returns the car timestamp"""
        return self.__timestamp

    def __str__(self):
        """Makes a printable string representing the car and returns it"""
        return "Car No: {}, Race Position: {}, Distance Travelled".format(self.__car_index,
                                                                          self.__position,
                                                                          self.distance_travelled)
