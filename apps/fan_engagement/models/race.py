import json
import random
import math
from models.car import Car
from models.car_coordinates import CarCoordinates
import paho.mqtt.client as mqtt
# Constants for a race
DRS_DISTANCE = 2
DRS_ZONE = 0.01
# Probability of messages
DRS_MESSAGE_PROB = 5
TEAM_RADIO_MESSAGE_PROB = 10
WEATHER_MESSAGE_PROB = 1 #1/1000


class Race:
    def __init__(self, client: mqtt.Client, car_topic, event_topic):
        self.__cars = {}  # Using a dictionary for fast search
        self.__client = client
        self.__car_positions = []
        self.__race_distance = 0
        self.__car_topic = car_topic
        self.__event_topic = event_topic
        with open('messages/overtakes.json') as file:
            self.__overtakes_reactions = json.load(file)
        with open('messages/drs.json') as file:
            self.__drs_messages = json.load(file)
        with open('messages/team_radios.json') as file:
            self.__team_radios = json.load(file)
        with open('messages/weather.json') as file:
            self.__weather = json.load(file)

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
            car_to_update.update_car_coordinates(car_coordinates)
            self.__assign_position(float(car_coordinates.get('timestamp')))
            # Reporting
            if car_to_update.get_car_position() != 0:
                self.publish_car_status(car_to_update.generate_position_report())
            self.publish_car_status(car_to_update.generate_speed_report())
        else:
            pass

    def __assign_position(self, timestamp: float):
        car_positions = list(self.__cars.values())
        # Loading the "old" car positions list to check if there is a change
        old_positions = self.__car_positions
        # We order the cars by the distance covered in the time that
        car_positions.sort(key=lambda car: car.distance_travelled, reverse=True)
        position = 1
        for c in car_positions:
            c.set_car_position(position)
            position += 1
        # Adding more and more interesting events
        self.__race_distance = car_positions[0].distance_travelled
        self.__throw_event_if_positions_changed(car_positions, old_positions, timestamp)
        self.__car_positions = car_positions
        #Weather events
        self.__throw_weather_events(timestamp)
        if self.__race_distance > DRS_DISTANCE:
            # DRS events
            self.__throw_drs_events(timestamp)

    def __throw_drs_events(self, timestamp):
        for i in range(0, len(self.__car_positions)-1):
            if math.fabs(self.__car_positions[i].distance_travelled -
                         self.__car_positions[i+1].distance_travelled) < DRS_ZONE:
                n = random.randint(0, 100)
                if n < DRS_MESSAGE_PROB:
                    event = {
                        'timestamp': timestamp,
                        'text': self.__drs_messages[random.randint(0, len(self.__drs_messages))]
                                .format(self.__car_positions[i].get_car_index())
                    }
                    self.publish_event(json.dumps(event))

    def __throw_team_radios(self, car_index, timestamp):
        n = random.randint(0, 100)
        # Rare event
        if n < TEAM_RADIO_MESSAGE_PROB:
            event = {
                'timestamp': timestamp,
                'text': self.__team_radios[random.randint(0, len(self.__team_radios))]
                        .format(car_index)
            }
            self.publish_event(json.dumps(event))

    def __throw_weather_events(self, timestamp):
        n = random.randint(0, 1000) #Rare event
        if n < WEATHER_MESSAGE_PROB:
            event = {
                'timestamp': timestamp,
                'text': self.__weather[random.randint(0, len(self.__weather))]
            }
            self.publish_event(json.dumps(event))

    def __throw_event_if_positions_changed(self, car_positions, old_positions, timestamp: float):
        discrepant_car_indices = []
        self.__obtain_position_changes(car_positions, discrepant_car_indices, old_positions)
        if discrepant_car_indices and len(discrepant_car_indices) >= 2:
            for i in range(0, len(discrepant_car_indices)-1):
                event = {
                    'timestamp': timestamp,
                    'text': self.__overtakes_reactions
                            [random.randint(0, len(self.__overtakes_reactions))]
                            .format(str(discrepant_car_indices[i]),
                                    str(discrepant_car_indices[i+1]))
                }
                self.publish_event(json.dumps(event))
                self.__throw_team_radios(discrepant_car_indices[i], timestamp)

    @staticmethod
    def __obtain_position_changes(car_positions, discrepant_car_indices, old_positions):
        for c in car_positions:
            if c in old_positions:
                if car_positions.index(c) != old_positions.index(c):
                    discrepant_car_indices.append(c.get_car_index())

    def publish_car_status(self, report):
        self.__client.publish(topic=self.__car_topic, payload=report)

    def publish_event(self, event):
        self.__client.publish(topic=self.__event_topic, payload=event)

    def get_participants(self):
        return self.__cars

    def get_race_distance(self):
        return self.__race_distance

    def get_client(self):
        return self.__client
