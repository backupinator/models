'''Base model for databases.'''

import peewee # pylint: disable=E0401

class ClientBaseModel(peewee.Model):
    '''A base model for client database.'''
    class Meta:
        '''Tell peewee where database is.'''
        database = peewee.SqliteDatabase('client/client.db')

class ServerBaseModel(peewee.Model):
    '''Base model for server database.'''
    class Meta:
        '''Tell peewee where database is.'''
        database = peewee.SqliteDatabase('server/server.db')

class TargetBaseModel(peewee.Model):
    '''Base model for target database.'''
    class Meta:
        '''Tell peewee where database is.'''
        database = peewee.SqliteDatabase('target/target.db')
