import mysql.connector
from mysql.connector import errorcode
import ConfigParser

from LocationWriter import LocationWriter

def runTestQuery(sql_conn, query):
    cursor = sql_conn.cursor(dictionary=True)

    for result in cursor.execute(query):
        if result.with_rows:
            print("Rows produced by statement '{}':".format(
                result.statement))
            print(result.fetchall())
        else:
            print("Number of rows affected by statement '{}': {}".format(
                result.statement, result.rowcount))

def connectToDB(db_config):
    _sql_location_qry = (
        "SELECT * FROM locations"
    )

    try:
        _sql_cnx = mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("Successfully connected to DB")
        runTestQuery(_sql_cnx, _sql_location_qry)

config = ConfigParser.RawConfigParser()
config.read('db_config')
configSections = config._sections
locationWriter = None

if 'db' in configSections:
    db_config = configSections.get('db')
    db_config.pop('__name__', None)
    locationWriter = LocationWriter(db_config)
    locationWriter.connectToDatabase()

    testLocation = {
        "timestamp": 1479605501999,
        "lat": 41.4941174956425,
        "long": 41.4941174956425,
        "speed": 0
    }
    locationWriter.writeLocation(testLocation)
else:
    print("No db section in config")

