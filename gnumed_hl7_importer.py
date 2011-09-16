__author__ = 'Jeffrey Leegon'

import os
import re
import hl7
import string
import hl7_interface_to_gnumed




def process_lab_message(message):
   # print hl7.ishl7(message)
    #print message
    h = hl7.parse(message)


    temp = h.segment('PID')[2]
    formatter_message ={'external_id': string.rstrip(str(temp[0]))}
    formatter_message['last_name']  = h.segment('PID')[5][1]
    formatter_message['first_name'] = h.segment('PID')[5][0]
    temp =  h.segment('PID')[8]
    formatter_message['gender'] =  string.rstrip(str(temp[0]))
    formatter_message['data_type'] = 'HL7'
    formatter_message['ordering_provider_information'] = " ".join(h.segment('OBR')[16])
    formatter_message['data'] = message

    #print formatter_message
    hl7_interface_to_gnumed.insert_unmatched_record(formatter_message)


file = open('test_data.hl7')

message = ''

find_message_header = re.compile(r"^MSH")

for n in file:
    if re.match(find_message_header, n):

        if message != '':
            process_lab_message(message)
        message = n + '\r'
    else:
        message = message + n + '\r'
  