from datetime import datetime
from glob import glob
import os
import shutil
import gnumed_error_writer

PROCESSED_FILE_EXTENSION = 'px'


def process_directory(extension, input_directory):
    """ finds all of the files of a given
    """
    input_directory = os.path.join(input_directory, "*." + extension)
    file_list = glob(input_directory)
    return file_list


def create_output_path(extension, file_path, output_directory, append_date_to_filename=False):
    """ Return a path to the out put directory with the requested extension. Append_Date to file in order to prevent duplicates from being over
    written
    """
    file_name = os.path.split(file_path)[1]
    file_wo_extension = os.path.splitext(file_name)[0]
    #Add date and time to the filename to help prevent duplicates
    output_filename = file_wo_extension

    if append_date_to_filename:
        output_filename += '-' + str(datetime.now())

    output_path = os.path.join(output_directory, output_filename + "." + extension)
    return output_path


def handle_processed_file(file_path, processed_file_dir=None):
    if processed_file_dir != None:
        try:
            move_processed_file(file_path, processed_file_dir)
        except IOError:
            #Attempt to rename the file so it won't be scanned later
            try:
                rename_processed_file(file_path)
            except IOError:
                error_message = "File %s could not be moved or renamed" % (file_path)
                gnumed_error_writer.write_error(error_message)
                exit(gnumed_error_writer.EXIT_FILE_OPERATION_ERROR)
            else:
                error_message = "File %s not moved. File renamed in its current directory with %s extension" % (
                file_path, PROCESSED_FILE_EXTENSION)
                gnumed_error_writer.write_error(error_message)
                exit(gnumed_error_writer.EXIT_FILE_OPERATION_ERROR)
    else:
        try:
            rename_processed_file(file_path)
        except IOError:
            error_message = "Could not rename file % with extension %s" % (file_path, PROCESSED_FILE_EXTENSION)



def move_processed_file(file_path, processed_file_dir):
    file_name = os.path.split(file_path)[1]
    move_file_path = os.path.join(processed_file_dir, file_name)
    shutil.move(file_path, move_file_path)


def rename_processed_file(file_path):
    temp_name = file_path + "." + PROCESSED_FILE_EXTENSION
    shutil.move(file_path, temp_name)