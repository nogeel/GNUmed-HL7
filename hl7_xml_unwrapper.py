from xml.etree import ElementTree
import sys
import gnumed_error_writer
import hl7_importer_file_directory_utilities

move_files = False


def process_xml_file(in_file, out_file, move_file_path=''):
    """ Opens the xml file  pulls out all of the hl7 messages in the file , then writes them to a text file. If a move_file_path
    is provided, it function moves the xml file to the given directory, otherwise it appends '.px' to all XML files that have been processed."""

    try:
        e_tree = ElementTree.parse(in_file)
    except:
        gnumed_error_writer.write_error("Not a valid XML file")
        exit(gnumed_error_writer.EXIT_CODE_INVALID_XML)


    # Grab all messages in the XML document
    messages = e_tree.findall('.//Message')

    # Check to see if the file is complete.
    # Looks at the MessageCount attribute in the root node and compare with the number of Message nodes
    stated_number = e_tree._root.attrib['MessageCount']
    if (len(messages) != int(stated_number)):
        error_message = "Number of message in %s do not match: Listed: %s\t Actual: %s" % (
        in_file,(len(messages)), str(stated_number))
        gnumed_error_writer.write_error(error_message)
        exit(gnumed_error_writer.EXIT_CODE_MISMATCH)

    #Write HL7 messages to  an HL7 file
    try:
        with open(out_file, 'w') as hl7_file:
            for node in messages:
                hl7_file.write(node.text)
    except IOError:
        error_message = "Could not open file %s" % out_file
        gnumed_error_writer.write_error(error_message)
        exit(gnumed_error_writer.EXIT_FILE_OPERATION_ERROR)


def process_xml_directory(input_directory, hl7_directory, processed_file_dir=None):
    try:
        xml_files = hl7_importer_file_directory_utilities.process_directory('xml', input_directory)
    except IOError:
        error_message = "An error occurred trying to retrieve the xml file contents of the directory: %s." % (
            input_directory)
        gnumed_error_writer.write_error(error_message)
        exit(gnumed_error_writer.EXIT_FILE_OPERATION_ERROR)
    else:

    # Process each file.
        for n in xml_files:
            hl7_path = hl7_importer_file_directory_utilities.create_output_path('hl7', n, hl7_directory, True)

            process_xml_file(n, hl7_path)
            hl7_importer_file_directory_utilities.handle_processed_file(n, processed_file_dir)


#Search for XML files located in the specified directory
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "There are not enough parameters:"
        print "python hl7_xml_unwrapper.py [input directory] [hl7 files directory]"
        print "OR"
        print "python hl7_xml_unwrapper.py [input directory] [hl7 files directory] [xml files directory]"

    if len(sys.argv) == 3:
        process_xml_directory(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        move_files = True
        process_xml_directory(sys.argv[1], sys.argv[2], sys.argv[3])