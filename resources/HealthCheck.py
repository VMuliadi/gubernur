from flask import Flask
from flask_restful import Resource, Api
from libs.db import *
import json

class HealthCheck(Resource):
    def get(self):
        return {'healthy':True}
