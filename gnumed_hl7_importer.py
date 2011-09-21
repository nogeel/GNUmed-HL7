__author__ = 'Jeffrey Leegon'

import re
import hl7
import string
import hl7_interface_to_gnumed


def process_lab_message(message):
    '''Processes and HL7 lab message. Pulls out the necessary data for the clin.incoming_data_unmatched
        into a dictionary along with the raw message then passes it on to the interface to be put in the database.
    '''

    h = hl7.parse(message)

   # temp = h.segment('PID')[2][0]
    formatter_message = {}
    formatter_message['external_id'] = handle_empty(string.rstrip(h.segment('PID')[2][0]))
    formatter_message['last_name'] = handle_empty(h.segment('PID')[5][0])

    formatter_message['first_name'] = handle_empty( h.segment('PID')[5][1] )

    #See if the message has a middle name that will also go into the first name column in the table
    if len(h.segment('PID')[5]) < 2:
        formatter_message['first_name'] +=  " " + h.segment('PID')[5][2]

    #If Gender equals 'U' leave the value null
    #temp = h.segment('PID')[8][0]
    gender = string.rstrip(h.segment('PID')[8][0])
    if (gender.upper() == 'M') or (gender.upper() == 'F'):
        formatter_message['gender'] = gender
    else:
         formatter_message['gender'] = None

    formatter_message['data_type'] = 'HL7'
    
    formatter_message['ordering_provider_information'] = handle_empty(" ".join(h.segment('OBR')[16]))
    formatter_message['data'] = message

    formatter_message['request_id'] = handle_empty(h.segment('ORC')[3][0])


    #Build the other info information
    temp_list = [h.segment('PID')[2][0], h.segment('PID')[3][0], h.segment('PID')[4][0]]
    if len(h.segment('PID'))> 12:
        temp_list.append(h.segment('PID')[13][0])
    temp_list = [ w.strip() for w in temp_list if len(w) != 0]
    formatter_message['other_info'] = " ".join(temp_list)

    hl7_interface_to_gnumed.insert_unmatched_record(formatter_message)


def handle_empty(segment):
    """ Sees if the segment is an empty string. If it is converts the segment to Python's None
    """
    if len(segment) == 0:
        return None
    else:
        return segment

def gnumed_hl7_importer(file_name):
    """ Goes through the file to find each HL7 message then passes it on to process_lab_message to extract t
    he specifically needed information from the database to be imported into GNUMed
    """
    file = open(file_name)

    message = ''

    find_message_header = re.compile(r"^MSH")
    #TODO Have it be able to process both a directory or an individual file
    for n in file:
        if re.match(find_message_header, n):
            if message != '':
                process_lab_message(message)
            message = n + '\r'
        else:
            message = message + n + '\r'


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print "Systax is python gnumed_hl7_importer.py hl7_file_path"
    else:
        gnumed_hl7_importer(sys.argv[1])