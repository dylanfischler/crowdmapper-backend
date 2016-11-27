import mysql.connector
from mysql.connector import errorcode


class LocationWriter(object):
    def __init__(self, db_config):
        self._sql_cnx = None
        self.cursor = None
        self.db_config = db_config

    def connectToDatabase(self):
        try:
            self._sql_cnx = mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise mysql.connector.InterfaceError("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise mysql.connector.InterfaceError("Database does not exist")
            else:
                raise mysql.connector.Error(err)
        else:
            self.cursor = self._sql_cnx.cursor(dictionary=True)
            print("Successfully connected to DB")

    def writeLocation(self, locationDict):
        location_insert = (
            "INSERT INTO locations (`lat`, `long`, `timestamp`, `speed`) "
            "VALUES (%s, %s, %s, %s)"
        )
        data = (
            locationDict.get('lat'), locationDict.get('long'),
            locationDict.get('timestamp'), locationDict.get('speed')
        )

        try:
            self.cursor.execute(location_insert, data)
            locationId = self.cursor.lastrowid
            print("Inserted {}".format(locationId))
        except mysql.connector.Error as err:
            print("Could not insert location into database {}".format(err))

    def commitWrites(self):
        self._sql_cnx.commit()

    def closeWriter(self):
        self._sql_cnx.close()
        self.cursor.close()
