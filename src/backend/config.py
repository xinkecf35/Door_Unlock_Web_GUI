"""

Module to define configuration variables for Door Unlock API

"""

import confuse


class Config:
    config = confuse.Configuration('door-unlock-api')
    dbName = config['SQLITE_DB_NAME'].get(str)


