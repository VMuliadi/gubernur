import os
import plyvel
import logging

class DB(object):
    SUCCESS = 0
    ERROR = 1
    def __setattr__(self, *_):
        pass

DB = DB()

def db_init(db_name):
    if db_name is None:
        return DB.ERROR
    try:
        database = plyvel.DB(db_name, create_if_missing=True)
    except Exception as e:
        return DB.ERROR
    if database is None:
        logging.error('Database init error')
        return DB.ERROR
    else:
        logging.info('Database init OK')
        return database

def db_write(database, key, val):
    if database is None or key is None or val is None:
        return DB.ERROR
    try:
        database.put(bytes(key), bytes(val))
    except Exception as e:
        return DB.ERROR
    return DB.SUCCESS

def db_read(database, key):
    if database is None or key is None:
        return DB.ERROR
    try:
        data = database.get(bytes(key))
    except Exception as e:
        return DB.ERROR
    return data

# TODO:
## * db_snapshot
## * db_import
## ??
