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

    temp = h.segment('PID')[2]
    formatter_message = {'external_id': string.rstrip(str(temp[0]))}
    formatter_message['last_name'] = h.segment('PID')[5][1]
    formatter_message['first_name'] = h.segment('PID')[5][0]
    temp = h.segment('PID')[8]
    formatter_message['gender'] = string.rstrip(str(temp[0]))
    formatter_message['data_type'] = 'HL7'
    formatter_message['ordering_provider_information'] = " ".join(h.segment('OBR')[16])
    formatter_message['data'] = message

    hl7_interface_to_gnumed.insert_unmatched_record(formatter_message)


def gnumed_hl7_importer(file_name):
    file = open(file_name)

    message = ''

    find_message_header = re.compile(r"^MSH")

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