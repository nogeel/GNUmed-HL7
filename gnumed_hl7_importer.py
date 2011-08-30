__author__ = 'Jeffrey Leegon'

import os
import re
import hl7
import string




def process_lab_message(message):
   # print hl7.ishl7(message)
    #print message
    h = hl7.parse(message)

    temp = h.segment('PID')[2]
    external_id = string.rstrip(str(temp[0]))
    print external_id
    last_name  = h.segment('PID')[5][1]
    first_name = h.segment('PID')[5][0]
    temp =  h.segment('PID')[8]
    gender =  string.rstrip(str(temp[0]))
    data_type = 'HL7'
    data = message

    #print h.segment('PID')[7][0]
    ordering_provider_information = "\t".join(h.segment('OBR')[16])

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
  