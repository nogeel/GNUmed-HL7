__author__ = 'Jeffrey Leegon'

import psycopg2
import traceback




connection_string = "host='localhost' dbname='gnumed_v15' user='postgres' password='dogdogdog'"

#def create_connection():



def insert_unmatched_record(record_dictionary):

    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        insert_query = """SET TRANSACTION READ WRITE;
                    INSERT into clin.incoming_data_unmatched
                    (external_data_id, lastnames, firstnames, gender, type, requestor, data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s); """

        #print insert_query
        cursor.execute(insert_query,  (record_dictionary['external_id'],  record_dictionary['last_name'],
          record_dictionary['first_name'], record_dictionary['gender'],
          record_dictionary['data_type'],  record_dictionary['ordering_provider_information'], psycopg2.Binary(record_dictionary['data'])))
        conn.commit()
        cursor.close()
        conn.close()
    except:
        print "Something went wrong"
        print traceback.print_exc()

