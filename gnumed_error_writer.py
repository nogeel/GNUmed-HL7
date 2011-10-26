import psycopg2
from ConfigParser import SafeConfigParser
import traceback

CONFIG_FILE_NAME = 'gnumed_hl7_interface.cfg'
FK_STAFF = 1
INBOX_ITEM_TYPE=4

#ERROR Codes
EXIT_CODE_MISMATCH = 1
EXIT_CODE_CANNOT_OPEN_FILE = 1
EXIT_CODE_INVALID_XML = 1
EXIT_CODE_DB_ISSUE = 1
EXIT_FILE_OPERATION_ERROR =1

try:
    parser = SafeConfigParser()
    parser.read(CONFIG_FILE_NAME)
except:
    print "The configuration file for the database was not found."

connection_string = "host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (parser.get('db', 'host'),
                                                                                 parser.get('db', 'port'),
                                                                                 parser.get('db', 'dbname'),
                                                                                 parser.get('logging', 'lg_user'),
                                                                                 parser.get('logging', 'lg_pwd'))
#Error Messages

def write_error(error_message):

    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        insert_query = """SET TRANSACTION READ WRITE;
                    INSERT into dem.message_inbox
                    (fk_staff, fk_inbox_item_type, comment)
                    VALUES (%s, %s, %s); """

        #print insert_query
        cursor.execute(insert_query, (FK_STAFF,INBOX_ITEM_TYPE, error_message ))
        conn.commit()
        cursor.close()
        conn.close()
    except:
        #TODO Handle this error better.
        print "Something went wrong"
    
    print error_message + "\n"

#def handle_file_with_error(file_path, move_directory)

