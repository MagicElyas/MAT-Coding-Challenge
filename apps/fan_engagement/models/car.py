import json


class Car:
    def __init__(self, lat: float, long: float, car_index: int):
        self.__lat = lat
        self.__long = long
        self.__car_index = car_index
        self.distance_travelled = 0
        self.position = 0
        self.curr_speed = 0

    def generate_speed_report(self, ts):
        res = {
          'timestamp': ts,
          'carIndex': self.__car_index,
          'type': 'SPEED',
          'value': self.curr_speed
        }
        return json.dumps(res)

    def generate_position_report(self, ts):
        res = {
          'timestamp': ts,
          'carIndex': self.__car_index,
          'type': 'POSITION',
          'value': self.position
        }
        return json.dumps(res)

    def get_car_index(self):
        return self.__car_index
