import pygame 
import numpy 


class Weather:
    def __init__(self, wind_speed):
        self.wind_speed = wind_speed

    def apply_effect(self, airplane):
        pass  # No horizontal movement for the airplane