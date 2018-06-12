#!/usr/bin/env python3
import json


def get_param(param):
    with open('settings.json', 'r') as s:
        data = json.loads(s.read())
    return data[param]


def what_number_of_levels():
    return get_param("numberOfLevels")


def what_capacity_of_elevator():
    return get_param("capacityOfElevator")


def what_delay_between_levels():
    return get_param("delayBetweenLevelsInSeconds")



