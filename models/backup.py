'''Define Backup model for databases.'''

import json
import configparser

import requests
import peewee # pylint: disable=E0401

from models import ClientBaseModel, ServerBaseModel, TargetBaseModel
from models import ClientClient, ServerClient, TargetClient
from models import ClientTarget, ServerTarget, TargetTarget
from models import ClientFile, ServerFile, TargetFile

class BaseBackup(peewee.Model):
    '''Define fields common to all databases.'''

    # Mark when backup is sent
    time_sent = peewee.DateTimeField(null=True, default=None)

    # The backup is not complete until we hear back that it completed.
    # The backup did not fail unless we hear back that it failed.
    is_complete = peewee.BooleanField(default=False)
    did_fail = peewee.BooleanField(default=False)

    # When the backup is pronounced DONE!
    time_done = peewee.DateTimeField(null=True, default=None)

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'time_sent': str(self.time_sent),
            'path': self.file.path,
            'client': self.client.name,
            'target': self.target.name,
            'is_complete': self.is_complete,
            'did_fail': self.did_fail,
            'time_done': str(self.time_done),
        })

class ClientBackup(ClientBaseModel, BaseBackup):
    '''Client's version of Backup model.'''

    # A client owns this backup job
    client = peewee.ForeignKeyField(ClientClient)

    # A file is being backed up for this backup job
    file = peewee.ForeignKeyField(ClientFile)

    # This backup is being sent to a target
    target = peewee.ForeignKeyField(ClientTarget)

    def send_to_server(self):
        '''Send backup job to server.'''

        # Create a file stream to hold file contents. The Backup
        # object data will be stored in the headers
        backup_str = json.dumps({
            'client_name:': self.client.name,
            'target_name': self.target.name,
            'hash_path': self.file.hash_path,
            'time_sent': str(self.time_sent),
        })
        hdrs = {
            'Backupinator-Info': backup_str
        }

        # Lookup server address
        config = configparser.ConfigParser()
        config.read('config.ini')
        server_address = config['DEFAULT']['server_address']
        endpoint = config['DEFAULT']['upload_endpoint']

        # Stream file to server
        # see https://2.python-requests.org//en/master/user/advanced/
        # #streaming-uploads
        with open(self.file.path, 'rb') as f:
            _resp = requests.post(
                server_address + endpoint, data=f, headers=hdrs)

class ServerBackup(ServerBaseModel, BaseBackup):
    '''Server's version of Backup model.'''

    client = peewee.ForeignKeyField(ServerClient)
    file = peewee.ForeignKeyField(ServerFile)
    target = peewee.ForeignKeyField(ServerTarget)

class TargetBackup(TargetBaseModel, BaseBackup):
    '''Target's version of Backup model.'''

    client = peewee.ForeignKeyField(TargetClient)
    file = peewee.ForeignKeyField(TargetFile)
    target = peewee.ForeignKeyField(TargetTarget)
