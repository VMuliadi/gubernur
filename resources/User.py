import re
import datetime
import functools
import jwt
from flask import Flask, request
from flask_restful import Resource, Api, abort
from werkzeug.security import generate_password_hash, check_password_hash
from libs.db import *
from models.User import User
import json

class Register(Resource):
    def post(self):
        self.db = db_init('users')

        # post data
        user = User(request.form['name'],
                    request.form['email'],
                    request.form['password'])

        # sanity check
        if user.check() == False:
            abort(400, message='request not valid.')
        if not re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', user.email):
            abort(400, message='email is not valid.')
        if len(user.password) < 8:
            abort(400, message='password is too short.')
        if (db_read(self.db, user.email) != None and db_read(self.db, user.email) != 1):
            abort(400, message='email is alread used.')
        else:
            user.password = generate_password_hash(user.password)
            db_write(self.db, user.email, user)

        exp = datetime.datetime.utcnow() + datetime.timedelta(days=3)
        encoded = jwt.encode({'email': user.email, 'exp': exp},
                             'supersecret', algorithm='HS256')

        print 'Activation Code:'
        print format(encoded.decode('utf-8'))

        # TODO: send email, or slack, or sms, or any
        return {'username': user.name, 'active': user.active}, 201

class Activate(Resource):
    def put(self):
        self.db = db_init('users')
        activation_code = request.form['activation_code']
        try:
            decoded = jwt.decode(activation_code, 'supersecret', algorithms='HS256')
        except jwt.DecodeError:
            abort(400, message='Activation code is not valid.')
        except jwt.ExpiredSignatureError:
            abort(400, message='Activation code is expired.')

        email = decoded['email']

        # update user active
        user = json.loads(db_read(self.db, email))
        user.update({"active":True})

        db_write(self.db, email, json.dumps(user))
        return {'email': email, 'active': True}

class Login(Resource):
    def post(self):
        self.db = db_init('users')
        email = request.form['email']
        password = request.form['password']

        user = json.loads(db_read(self.db, email))

        if user == DB.ERROR:
            abort(400, message='User is not found.')
        if not check_password_hash(user['password'], password):
            abort(400, message='Password is incorrect.')

        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        encoded = jwt.encode({'email': email, 'exp': exp},
                             'supersecret', algorithm='HS256')

        return {'email': user['email'], 'token': encoded.decode('utf-8'),
                'active': user['active']}
