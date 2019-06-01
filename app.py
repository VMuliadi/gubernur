from flask import Flask
from flask_restful import Resource, Api
from resources.HealthCheck import *
from resources.User import *

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

api.add_resource(HealthCheck, '/healthz')
api.add_resource(Register, '/register')
api.add_resource(Activate, '/activate')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True)
