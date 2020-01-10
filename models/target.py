'''Define target model for databases.'''

import json
from datetime import datetime

import peewee # pylint: disable=E0401

from models import ClientBaseModel, ServerBaseModel, TargetBaseModel

class BaseTarget(peewee.Model):
    '''Define fields common to all databases.'''

    name = peewee.CharField(unique=True)
    last_active = peewee.DateTimeField(default=datetime.now())

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'last_active': str(self.last_active),
        })

class ClientTarget(ClientBaseModel, BaseTarget):
    '''Client's version of the Target model.'''

class ServerTarget(ServerBaseModel, BaseTarget):
    '''Server's version of the Target model.'''

class TargetTarget(TargetBaseModel, BaseTarget):
    '''Target's version of the Target model.'''
