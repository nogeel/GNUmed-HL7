from xml.etree import ElementTree
import sys
import glob
import os
import os.path
import shutil
from datetime import datetime
import GNUMedErrorWriter

__author__ = 'Jeffrey Leegon'

move_files = False


def process_xml_file(in_file, out_file, move_file_path=''):
    """ Opens the xml file  pulls out all of the hl7 messages in the file , then writes them to a text file. If a move_file_path
    is provided, it function moves the xml file to the given directory, otherwise it appends '.px' to all XML files that have been processed."""

    try:
        e_tree = ElementTree.parse(in_file)
    except:
        GNUMedErrorWriter.write_error("Not a valid XML file")


    # Grab all messages in the XML document
    messages = e_tree.findall('.//Message')


    # Check to see if the file is complete.
    # Looks at the MessageCount attribute in the root node and compare with the number of Message nodes
    stated_number = e_tree._root.attrib['MessageCount']
    print "Do the numbers match?\t" + str((len(messages) == int(stated_number)))

    #Write HL7 messages to  an HL7 file
    try:
        with open(out_file, 'w') as hl7_file:
            for node in messages:
                hl7_file.write(node.text)
    except IOError:
        GNUMedErrorWriter.write_error("Could not open the file")

    try:
        if move_files:
            shutil.move(in_file, move_file_path)
        else:
            temp_name = in_file + ".px"
            shutil.move(in_file, temp_name)
    except IOError:
        GNUMedErrorWriter.write_error(
            "File could not be moved to the specified directory. filename will be changed instead.")


def process_directory(input_directory, hl7_directory, processed_file_dir=''):
    input_directory = os.path.join(input_directory, "*.xml")
    xml_files = glob.glob(input_directory)
    print input_directory
    print xml_files
    # Process each file.
    for n in xml_files:
        print "Processing file:" + n
        file_name = os.path.split(n)[1]
        file_wo_extension = os.path.splitext(file_name)[0]
        #Add date and time to the filename to help prevent duplicates
        dated_filename = file_wo_extension + '-' + str(datetime.now())
        hl7_path = os.path.join(hl7_directory, dated_filename + ".hl7")
        if move_files:
            move_path = os.path.join(processed_file_dir, file_name)
            process_xml_file(n, hl7_path, move_path)
        else:
            process_xml_file(n, hl7_path)

#Search for XML files located in the specified directory
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "There are not enough parameters:"
        print "python hl7_xml_unwrapper.py [input directory] [hl7 files directory]"
        print "OR"
        print "python hl7_xml_unwrapper.py [input directory] [hl7 files directory] [xml files directory]"

    if len(sys.argv) == 3:
        process_directory(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        move_files = True
        process_directory(sys.argv[1], sys.argv[2], sys.argv[3])