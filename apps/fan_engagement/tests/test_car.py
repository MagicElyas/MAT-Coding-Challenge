from models.car import Car
import pytest
import json


class TestCar:
    # Tests for generate speed report
    def test_generate_speed_report_when_called__returns_valid_object(self):
        car = Car(0, 0, 0, 1)
        res = car.generate_speed_report()
        assert res

    def test_generate_speed_report_when_called__returns_speed_type_report(self):
        car = Car(0, 0, 0, 1)
        res = car.generate_speed_report()
        res = json.loads(res)
        assert res['type'] == 'SPEED'

    def test_generate_speed_report_when_called_result_has_same_car_index(self):
        car = Car(0, 0, 0, 1)
        res = car.generate_speed_report()
        res = json.loads(res)
        assert res['carIndex'] == 1

    def test_generate_speed_report_when_called_result_has_same_timestamp(self):
        car = Car(0, 0, 0, 1)
        res = car.generate_speed_report()
        res = json.loads(res)
        assert res['timestamp'] == 0
    
    def test_generate_speed_report_when_called_result_0_mph(self):
        car = Car(0, 0, 0, 1)
        res = car.generate_speed_report()
        res = json.loads(res)
        assert res['value'] == 0
    
    # Tests for generate position
    
    def test_generate_position_report_when_called__returns_valid_object(self):
        car = Car(0, 0, 0, 1)
        res = car.generate_position_report()
        assert res is not None

    def test_generate_position_report_when_called__returns_position_type_report(self):
        car = Car(0, 0, 0, 1)
        res = car.generate_position_report()
        res = json.loads(res)
        assert res['type'] == 'POSITION'

    def test_generate_position_report_when_called_result_has_same_car_index(self):
        car = Car(0, 0, 0, 1)
        res = car.generate_position_report()
        res = json.loads(res)
        assert res['carIndex'] == 1

    def test_generate_position_report_when_called_result_has_same_timestamp(self):
        car = Car(0, 0, 0, 1)
        res = car.generate_position_report()
        res = json.loads(res)
        assert res['timestamp'] == 0
    
    def test_generate_position_report_when_called_result_0_mph(self):
        car = Car(0, 0, 0, 1)
        res = car.generate_position_report()
        res = json.loads(res)
        assert res['value'] == 0
    
    # Tests for update car coordinates

    def test_update_car_coordinates_when_called_with_same_coords_distance_equals_0(self):
        car = Car(0, 0, 0, 1)
        car_coords = {
            'timestamp': 1,
            'carIndex': 1,
            'location':{
                'lat':0,
                'long':0
            }
        }
        car.update_car_coordinates(car_coords)
        assert car.distance_travelled == 0

    def test_update_car_coordinates_when_called_with_same_coords_speed_equals_0(self):
        car = Car(0, 0, 0, 1)
        car_coords = {
            'timestamp': 1,
            'carIndex': 1,
            'location':{
                'lat':0,
                'long':0
            }
        }
        car.update_car_coordinates(car_coords)
        assert car.curr_speed == 0
    
    def test_update_car_coordinates_when_called_with_same_ts_distance_equals_0(self):
        car = Car(0, 0, 0, 1)
        car_coords = {
            'timestamp': 0,
            'carIndex': 1,
            'location':{
                'lat':1,
                'long':1
            }
        }
        car.update_car_coordinates(car_coords)
        assert car.distance_travelled == 0
    
    def test_update_car_coordinates_when_called_normally_returns_speed_correctly(self):
        car = Car(0, 0, 0, 1)
        car_coords = {
            'timestamp': 3600000,
            'carIndex': 1,
            'location':{
                'lat':0.01,
                'long':0
            }
        }
        # Calculated value of this transtion = 0.6870766960504942
        car.update_car_coordinates(car_coords)
        assert car.curr_speed == 0.6870766960504942
    
    def test_update_car_coordinates_when_called_normally_returns_correct_distance_travelled(self):
        car = Car(0, 0, 0, 1)
        car_coords = {
            'timestamp': 3600000,
            'carIndex': 1,
            'location':{
                'lat':0.01,
                'long':0
            }
        }
        # Calculated value of this transtion = 0.6870766960504942
        car.update_car_coordinates(car_coords)
        assert car.distance_travelled == 0.6870766960504942

    def test_update_car_coordinates_when_called_normally_returns_updated_ts(self):
        car = Car(0, 0, 0, 1)
        car_coords = {
            'timestamp': 3600000,
            'carIndex': 1,
            'location':{
                'lat':0.01,
                'long':0
            }
        }
        car.update_car_coordinates(car_coords)
        assert car.get_car_timestamp() == 3600000

    def test_update_car_coordinates_when_called_normally2times_returns_updated_ts(self):
        car = Car(0, 0, 0, 1)
        car_coords = {
            'timestamp': 3600000,
            'carIndex': 1,
            'location':{
                'lat':0.01,
                'long':0
            }
        }
        car.update_car_coordinates(car_coords)
        car_coords = {
            'timestamp': 7200000,
            'carIndex': 1,
            'location':{
                'lat':0.02,
                'long':0
            }
        }
        car.update_car_coordinates(car_coords)
        assert car.get_car_timestamp() == 7200000

    def test_update_car_coordinates_when_called_normally2times_returns_updated_distance(self):
        car = Car(0, 0, 0, 1)
        car_coords = {
            'timestamp': 3600000,
            'carIndex': 1,
            'location':{
                'lat':0.01,
                'long':0
            }
        }
        car.update_car_coordinates(car_coords)
        car_coords = {
            'timestamp': 7200000,
            'carIndex': 1,
            'location':{
                'lat':0.02,
                'long':0
            }
        }
        car.update_car_coordinates(car_coords)
        # Operating with floats, so we round to the 5 more significant digits
        assert round(car.distance_travelled,5) == round(2*0.6870766960504942,5)

    def test_update_car_coordinates_when_called_normally2times_returns_updated_speed(self):
        car = Car(0, 0, 0, 1)
        car_coords = {
            'timestamp': 3600000,
            'carIndex': 1,
            'location':{
                'lat':0.01,
                'long':0
            }
        }
        car.update_car_coordinates(car_coords)
        car_coords = {
            'timestamp': 7200000,
            'carIndex': 1,
            'location':{
                'lat':0.02,
                'long':0
            }
        }
        car.update_car_coordinates(car_coords)
        # Operating with floats, so we round to the 5 more significant digits
        assert round(car.distance_travelled,5) == round(2*0.6870766960504942,5)


    