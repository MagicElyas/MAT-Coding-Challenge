from apps.fan_engagement.models.car import Car
from apps.fan_engagement.models.car_coordinates import CarCoordinates

class Race:
    def __init__(self):
        self.__cars = {}  # Using a dictionary for fast search

    def add_car_to_the_race(self, car: Car):
        if car not in self.__cars:
            self.__cars[car.car_index] = car

    def update_car_info(self, car_status: dict):
        if CarCoordinates.validate_car_coordinates(car_status):
            car_to_update = None
            if car_status.get('carIndex') in self.__cars:
                car_to_update = self.__cars.get(car_status.get('carIndex'))
            else:
                car_to_update = Car(float(car_status['location']['lat']),
                                    float(car_status['location']['long']),
                                    int(car_status['carIndex']))
                self.add_car_to_the_race(car_to_update)
            # TODO: Some logic to update the distance and position of the car
        else:
            pass



    def publish_event(self, event: dict):
        # TODO: Publish event to the event queues, simply json.dumps
        pass