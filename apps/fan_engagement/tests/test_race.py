import pytest
from models.race import Race
import paho.mqtt.client as mqtt
class TestRace:
  def test_generate_race_returns_empty_cars(self):
    race = Race(None, '','')
    assert race.get_participants() == {}
  
  def test_generate_race_returns_zero_distance(self):
    race = Race(None, '','')
    assert race.get_race_distance() == 0
  
  def test_generate_race_with_null_client_returns_null_client(self):
    race = Race(None, '','')
    assert race.get_client() is None
  
  def test_generate_race_and_add_car_correctly(self):
    client = mqtt.Client('test')
    race = Race(client, 't1','t2')
    car_coords = {
            'timestamp': 1,
            'carIndex': 1,
            'location':{
                'lat':0,
                'long':0
            }
        }
    race.update_car_info(car_coords)
    assert len(race.get_participants().values()) == 1

  def test_generate_race_update_car_info_updates_correctly(self):
    client = mqtt.Client('test')
    race = Race(client, 't1','t2')
    car_coords = {
            'timestamp': 1,
            'carIndex': 1,
            'location':{
                'lat':0,
                'long':0
            }
        }
    race.update_car_info(car_coords)
    car_coords = {
            'timestamp': 2,
            'carIndex': 1,
            'location':{
                'lat':0,
                'long':0
            }
        }
    race.update_car_info(car_coords)
    assert len(race.get_participants().values()) == 1
    assert list(race.get_participants().values())[0].get_car_timestamp() == 2

  def test_generate_race_update_with_invalid_json_does_not_change(self):
    client = mqtt.Client('test')
    race = Race(client, 't1','t2')
    car_coords = {
            #'timestamp': 1, Incorrect car_coords
            'carIndex': 1,
            'location':{
                'lat':0,
                'long':0
            }
        }
    race.update_car_info(car_coords)
    assert len(race.get_participants().values()) == 0 

  def test_generate_race_add_two_cars_and_update_one_makes_him_leader(self):
    client = mqtt.Client('test')
    race = Race(client, 't1','t2')
    c1 = {
            'timestamp': 1, 
            'carIndex': 1,
            'location':{
                'lat':0,
                'long':0
            }
        }
    race.update_car_info(c1)
    c2 = {
            'timestamp': 1, 
            'carIndex': 2,
            'location':{
                'lat':0,
                'long':0
            }
        }
    race.update_car_info(c2)
    c2['timestamp'] = 3
    c2['location'] = {'lat': 0.1, 'long':0.1}
    race.update_car_info(c2)

    assert len(race.get_participants().values()) == 2
    assert race.get_participants()[2].get_car_position() == 1
  
  def test_generate_race_a_car_has_a_position_assigned_always(self):
    client = mqtt.Client('test')
    race = Race(client, 't1','t2')
    c1 = {
            'timestamp': 1, 
            'carIndex': 1,
            'location':{
                'lat':0,
                'long':0
            }
        }
    race.update_car_info(c1)

    assert len(race.get_participants().values()) == 1
    assert race.get_participants()[1].get_car_position() == 1


  def test_generate_race_add_two_cars_both_have_positions(self):
    client = mqtt.Client('test')
    race = Race(client, 't1','t2')
    c1 = {
            'timestamp': 1, 
            'carIndex': 1,
            'location':{
                'lat':0,
                'long':0
            }
        }
    race.update_car_info(c1)
    c2 = {
            'timestamp': 1, 
            'carIndex': 2,
            'location':{
                'lat':0,
                'long':0
            }
        }
    race.update_car_info(c2)

    assert len(race.get_participants().values()) == 2
    assert race.get_participants()[1].get_car_position() == 1
    assert race.get_participants()[2].get_car_position() == 2