from database_utils import sql_query
import json
from transliteration import translit


def geo_object_to_json(geo_object: tuple): 
    '''
    Convert geographical object to JSON string.
    Arguments:
    - geo_object: tuple of values, describing geographical object.
    Return:
    JSON formatted string.
    '''

    properties = (
        'geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude', 
        'feature_class', 'feature_code', 'country_code', 'cc2', 'admin1_code', 
        'admin2 code', 'admin3 code', 'admin4 code','population', 'elevation',
        'dem', 'timezone', 'modification date'
    )
    object_dict = {}
    for i in range(min(len(properties), len(geo_object))):
        object_dict[properties[i]] = geo_object[i]
    
    return json.dumps(object_dict, indent=2, ensure_ascii=False)


def get_object_info(geonameid: int):
    '''
    Get information about geographical object with provided id.
    Arguments:
    - geonameid: id of the object in database.
    Return:
    JSON formatted string with the object decsription or False if nothing found.
    '''

    objects_list = sql_query(
        '''
        select * from geonames 
        where geonameid = ?
        ''', (geonameid,)
    )
    
    if len(objects_list) == 0:
        return False

    return geo_object_to_json(objects_list[0])


def get_page(page_num: int, object_count: int):
    '''
    Get a list of geographical objects on given page in page view.
    Arguments:
    - page_num: number of page in page view.
    - object_count: count of objects on one page.
    Return:
    JSON formatted string - array of objects describing objects or False if page with given number wasn't found.
    '''
    
    if page_num < 1:
        return False
    if object_count < 1:
        return '[]'

    objects_list = sql_query(
        '''
        select * from geonames 
        order by geonameid asc 
        limit ? offset ?
        ''', (object_count, (page_num-1)*object_count)
    )
    if len(objects_list) == 0:
        return False

    return '[' + ',\n'.join(list(map(geo_object_to_json, objects_list))) + ']'


def get_objects_comparison(first_object_name: str, second_object_name: str):
    '''
    Get information about two geographical objects and their comparison of the latitude and time zone.
    Arguments:
    - first_object_name, second_object_name: russian names of objects.
    Return:
    JSON formatted string - array with two geographical objects and comparison object or False if any object wasn't found. 
    '''

    # List of tuples
    first_object_info = find_objects_by_name(translit(first_object_name))
    second_object_info = find_objects_by_name(translit(second_object_name))
    
    if len(first_object_info) == 0 or len(second_object_info) == 0:
        return False

    # Sort objects by population.
    first_object_info.sort(key=lambda x: x[14], reverse=True)
    second_object_info.sort(key=lambda x: x[14], reverse=True)
    
    comparison = {}

    # Compare the latitude.
    if first_object_info[0][4] > second_object_info[0][4]:
        comparison['north'] = first_object_info[0][2]
    elif first_object_info[0][4] < second_object_info[0][4]:
        comparison['north'] = second_object_info[0][2]
    else:
        comparison['north'] = [first_object_info[0][2], second_object_info[0][2]]

    # object_info[0][17] - name of time zone.
    first_object_time_offset = sql_query(
        'select raw_offset from time_zones where time_zone_id = ?', (first_object_info[0][17],)
    )
    second_object_time_offset = sql_query(
        'select raw_offset from time_zones where time_zone_id = ?', (second_object_info[0][17],)
    )

    if len(first_object_time_offset) == 0 or len(second_object_time_offset) == 0:
        comparison['time_difference'] = None
    else:
        comparison['time_difference'] = abs(first_object_time_offset[0][0] - second_object_time_offset[0][0])

    # Comparison dict is serialized to a JSON formatted string.
    return '[' + geo_object_to_json(first_object_info[0]) + ',\n' + geo_object_to_json(second_object_info[0]) + ',\n' + json.dumps(comparison, indent=2, ensure_ascii=False) + ']'


def find_objects_by_name(name_variants: list):
    '''
    Find all records in the database that relate to the objects with the specified names.
    Arguments:
    - name_variants: list of ascii names (latin).
    Return:
    List of tuples - records of geonames table. 
    '''

    result = []
    for name in name_variants:
        result.extend(
            sql_query(
                '''
                select * from geonames
                where asciiname = ?
                ''', (name,)
            )
        )
    return result
