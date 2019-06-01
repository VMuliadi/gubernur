from flask import Flask
from flask_restful import Resource, Api
import json

class User():
    name = None
    password = None
    email = None
    active = False

    def __init__(self, name, email, password):
        self.name = name
        self.password = password
        self.email = email
        self.active = False

    def check(self):
        if self.name == None or self.password == None or self.email == None:
            return False
        return True

    def __repr__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return json.dumps(self.__dict__)
