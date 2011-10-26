__author__ = 'Jeffrey Leegon'

import psycopg2
from ConfigParser import SafeConfigParser
import gnumed_error_writer


CONFIG_FILE_NAME = 'gnumed_hl7_interface.cfg'

try:
    parser = SafeConfigParser()
    parser.read(CONFIG_FILE_NAME)
except:
    print "The configuration file for the database was not found."

connection_string = "host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (parser.get('db', 'host'),
                                                                                 parser.get('db', 'port'),
                                                                                 parser.get('db', 'dbname'),
                                                                                 parser.get('db', 'user'),
                                                                                 parser.get('db', 'password'))


def insert_unmatched_record(record_dictionary):
    '''Inserts the record into the clin.incoming_data_unmatched directly into the GNUMed database. Takes in a dictionary containing
    the needed data.'''
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        insert_query = """SET TRANSACTION READ WRITE;
                    INSERT into clin.incoming_data_unmatched
                    (external_data_id, lastnames, firstnames, gender, type, requestor, request_id, other_info, data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); """

        #print insert_query
        cursor.execute(insert_query, (record_dictionary['external_id'], record_dictionary['last_name'],
                                      record_dictionary['first_name'], record_dictionary['gender'],
                                      record_dictionary['data_type'], record_dictionary['ordering_provider_information']
                                      , record_dictionary['request_id'], record_dictionary['other_info'],
                                      psycopg2.Binary(record_dictionary['data'])))
        conn.commit()
        cursor.close()
        conn.close()
    except:
        error_message = "And error occurred trying to insert record with request_id: \'%s\'\t and external_id: \'%s\'. "\
        % (record_dictionary['request_id'], record_dictionary['external_id'])
        gnumed_error_writer.write_error(error_message)
        exit(gnumed_error_writer.EXIT_CODE_DB_ISSUE)

