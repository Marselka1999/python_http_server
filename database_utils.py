import sqlite3

CONNECTION = None
CURSOR = None
GEONAMES_FILE_PATH = 'RU.txt'
TIME_ZONES_FILE_PATH = 'timeZones.txt'
DATABASE_PATH = 'geonames.sqlite'


def connection(function):
    '''
    Decorator for all functions, which require connection to the database.
    Check that connection is established, otherwise try to connect to database on DATABASE_PATH.

    sqlite3.connect(path) creates database on provided path or connects to it, returning connection object.
    '''
    def wrapper(*args, **kwargs):
        global CURSOR, CONNECTION, DATABASE_PATH
        if not (CURSOR and CONNECTION):
            CONNECTION = sqlite3.connect(DATABASE_PATH)
            CURSOR = CONNECTION.cursor()
        if not (CURSOR and CONNECTION):
            raise ConnectionError('Сonnection to the database is not established')

        return function(*args, **kwargs)

    return wrapper
    

def disconnect_database():
    '''
    Close connection to the DB.
    '''
    global CONNECTION, CURSOR
    if CONNECTION:
        CONNECTION.close()
        CONNECTION = None
    CURSOR = None


@connection
def create_tables():
    '''
    Create tables geonames and time_zones if they don't exist.
    '''
    sql_query(
        '''
        create table if not exists geonames (
            geonameid integer primary key, 
            name text not null,
            asciiname text not null,
            alternatenames text not null,
            latitude real not null,
            longitude real not null,
            feature_class text not null,
            feature_code text not null,
            country_code text not null,
            cc2 text not null,
            admin1_code text not null,
            admin2_code text not null,
            admin3_code text not null,
            admin4_code text not null,
            population integer not null,
            elevation integer not null,
            dem integer not null,
            timezone text not null,
            modification_date text not null
        )
        '''
    )
    sql_query(
        '''
        create table if not exists time_zones (
            country_code text not null,
            time_zone_id text primary key,
            gmt_offset real not null,
            dst_offset real not null,
            raw_offset real not null
        )
        '''
    )

@connection
def create_database():
    '''
    Create new database from files GEONAMES_FILE_PATH and TIME_ZONES_FILE_PATH on DATABASE_PATH.
    '''
    create_tables()

    with open(GEONAMES_FILE_PATH, 'r', encoding='utf-8') as file:
        while True:
            line = file.readline()
            if line:
                sql_query(
                    '''
                    insert into geonames values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', line.strip().split('\t')
                )
                break
            else:
                break
    
    with open(TIME_ZONES_FILE_PATH, 'r', encoding='utf-8') as file:
        while True:
            line = file.readline()
            if line:
                sql_query(
                    '''
                    insert into time_zones values (?,?,?,?,?)
                    ''', line.strip().split('\t')
                )
                break
            else:
                break

    disconnect_database()


@connection
def sql_query(query_template: str, wildcard_values: tuple = ()):
    '''
    Execute any SQL query.
    Arguments:
    - query_template: query string with the wildcards ("?"). 
        For example, "select * from geonames where geonameid = ?". 
        * Wildcards are not available for table names.
    - wildcard_values: tuple of values which substitute "?" signs in query string.
    Return:
    List of table records. Each record is a tuple even if query returned one value.
    '''
    CURSOR.execute(query_template, wildcard_values)
    CONNECTION.commit()
    return CURSOR.fetchall()

if __name__ == "__main__":
    # create_database()
    print("Database created successfully")