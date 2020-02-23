from apps.fan_engagement.models.car import Car
from apps.fan_engagement.models.car_coordinates import CarCoordinates
import paho.mqtt.client as mqtt

class Race:
    def __init__(self, client: mqtt.Client):
        self.__cars = {}  # Using a dictionary for fast search
        self.__client = client

    def __add_car_to_the_race(self, car: Car):
        self.__cars[car.get_car_index()] = car

    def update_car_info(self, car_coordinates: dict):
        if CarCoordinates.validate_car_coordinates(car_coordinates):
            if car_coordinates.get('carIndex') in self.__cars.keys():
                car_to_update = self.__cars.get(car_coordinates.get('carIndex'))

            else:
                car_to_update = Car(float(car_coordinates.get('location').get('lat')),
                                    float(car_coordinates.get('location').get('long')),
                                    float(car_coordinates.get('timestamp')),
                                    int(car_coordinates.get('carIndex')))
                self.__add_car_to_the_race(car_to_update)
            # TODO: Some logic to update the distance and position of the car
            car_to_update.update_car(car_coordinates)

            self.publish_car_status(car_to_update.generate_speed_report())
        else:
            pass

    def __calculate_position(self):
        # TODO: Calculate the position of the car
        pass

    def publish_car_status(self, report):
        self.__client.publish(topic='carStatus', payload=report)

    def publish_event(self, event: dict):
        # TODO: Publish event to the event queues, simply json.dumps
        pass
