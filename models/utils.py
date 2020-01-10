'''Utility functions for database models.'''

import hashlib

def _compute_checksum(filepath, buf_size=65536):
    '''Calculate the checksum of data located at filepath.'''
    # Split into chunks so we're not hard on memory
    sha1 = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest().encode('utf-8')
