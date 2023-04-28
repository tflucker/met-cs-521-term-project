import csv
from contact import Contact
import app_functions as af

def read_file(filepath):
    '''
        Opens a file at a certain filepath using the csv module. Then each
        line is validated to ensure it has the correct number of arguments
        to create a contact record. Each line is added to a set to ensure 
        uniqueness and then a contact is created from each line in the set.
        This list of contacts is then returned to the app.py
    '''
    data_list = []
    contact_set = set()
    id_list = []

    try:
        with open(filepath,'r') as file:
            reader = csv.reader(file)
            line_counter = 1
            for line in reader:
                # validate_line returns tuple(is_valid_bool, line_str)
                validation_results = tuple(validate_line(line, 
                    line_counter, id_list))
                # if valid line, then add to contact_set
                if validation_results[0]:
                    contact_set.add(validation_results[1])
                
                # increment line counter
                line_counter += 1
            
    except FileNotFoundError:
        print("File not found. Starting application with blank contact list.")
    except Exception:
        print("Invalid Data detected and no data has been imported.")

    else:
        print("LOG: Read {} lines in file: {}".format(line_counter-1, 
            filepath))
        # for each item in the set, check if length is 7 or 8
        for item in contact_set:
            values = str(item).split(",")
            # if length is 7 generate a unique id
            if len(values) == 7:
                # add unique id to list of values
                values.insert(0, af.generateUniqueID(id_list))
            # with full 8 parameter list, create new instance of contact
            # object with values, then add to data_list
            new_contact = Contact(values)
            data_list.append(new_contact)
    return data_list

def validate_line(line:list, line_counter:int, id_list:list)->tuple: 
    '''
        Validates line (type = list) by checking it has the proper number of
        arguments and is not the header line
    '''
    result = True
    # ignore the column header line 
    if line != ",".join(af.FIELD_NAMES):
        # check if line contains an id value, if so add it to 
        # id_list to ensure that any lines without an id will
        # generate a unique value
        if len(line) == 8:
            id_list.append(line[0])
        if len(line) == 7 or len(line) == 8:
            line_str = ",".join(line)
        else:
            result = False
            print("ERROR: Invalid number of arguments on line {}. {}"
                .format(
                    line_counter, 
                    "Data on this line not imported."))
    return (result,line_str)