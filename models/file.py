'''Define File model for databases.'''

import hashlib
import json

import peewee # pylint: disable=E0401

from models import ClientBaseModel, ServerBaseModel, TargetBaseModel
from models import ClientClient, ServerClient, TargetClient

from models.utils import _compute_checksum

# Static variable for hashing path
_DIGEST_SIZE = 16

class BaseFile(peewee.Model):
    '''Define fields common to all databases.'''

    # Path to file on the client's machine
    path = peewee.CharField(unique=True)

    # Hash of the path to the file so we can use it as filename when
    # we save the file
    hash_path = peewee.CharField(unique=True)

    # Keep track of file modifications
    last_modified = peewee.DateTimeField()

    @staticmethod
    def make_hash_path(path, client_name):
        '''Make a unique hash of the path for use as a filename.'''
        return hashlib.blake2b(
            path.encode(), person=client_name.encode(),
            digest_size=_DIGEST_SIZE).hexdigest().encode('utf-8')

class ClientFile(ClientBaseModel, BaseFile):
    '''Client's version of the File model.'''

    # Owned by a client:
    owner = peewee.ForeignKeyField(ClientClient)

    def __str__(self):
        return json.dumps({
            'path': self.path,
            'owner': self.owner.name,
            'last_modified': self.last_modified,
        })

    def compute_checksum(self):
        '''Generate a checksum for file stored on Client.'''
        return _compute_checksum(self.path)

class ServerFile(ServerBaseModel, BaseFile):
    '''Server's version of the File model.'''
    owner = peewee.ForeignKeyField(ServerClient)

    # Need to know where it's stored on the server
    server_path = peewee.CharField(unique=True)

    def compute_checksum(self):
        '''Generate checksum for a file stored on Server.'''
        return _compute_checksum(self.server_path)

class TargetFile(TargetBaseModel, BaseFile):
    '''Target's version of the File model.'''
    owner = peewee.ForeignKeyField(TargetClient)

    # Need to know wherer it's stored on the Target
    target_path = peewee.CharField(unique=True)

    def compute_checksum(self):
        '''Generate checksum for a file stored on Target.'''
        return _compute_checksum(self.target_path)
