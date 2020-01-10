'''Define a client model for databases.'''

import hashlib
import uuid
from datetime import datetime
import json

import peewee # pylint: disable=E0401

from models import ClientBaseModel, ServerBaseModel, TargetBaseModel

class BaseClient(peewee.Model):
    '''Define fields common to all databases.'''

    name = peewee.CharField(unique=True)
    last_active = peewee.DateTimeField(default=datetime.now())

class ClientClient(ClientBaseModel, BaseClient):
    '''The Client's version of Client model.'''

    email = peewee.CharField()
    password = peewee.CharField()
    # passphrase = peewee.CharField()

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'last_active': str(self.last_active),
        })

    @staticmethod
    def hash_password(password):
        '''Salt and hash password.'''
        salt = uuid.uuid4().hex
        return hashlib.sha512(
            (password + salt).encode()).hexdigest().encode('utf-8')

class ServerClient(ServerBaseModel, BaseClient):
    '''The Server's version of Client model.'''

class TargetClient(TargetBaseModel, BaseClient):
    '''The Target's version of the Client model.'''
