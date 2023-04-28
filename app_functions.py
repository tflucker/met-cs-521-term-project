import time
import os
import random

from contact import *
import csv_filereader as fr

FIELD_NAMES = ["ID","FIRST_NAME", "LAST_NAME", "PHONE_NUMBER", "EMAIL", 
    "COMPANY", "TITLE", "RELATIONSHIP"]


def display_help_info():
    '''
        Display helpful information for each command.
    '''

    command_descriptions = '''
    "ADD" - Allows the user to create a new Contact record based on their 
    input. This input is required to fill the first_name, last_name, 
    phone_number, email, and relationship. Values for the company and title 
    fields are optional. Each field is validated to ensure that the input is 
    the correct data type, a proper length, and if that field is required or 
    not. All fields must have values less than 30 characters, the 
    phone_number and email fields require special formats, and the relationship
    field only accepts certain values. A unique ID is assigned when all values
    for the contact pass their respective validations. After the data is added, 
    the user is allowed to enter a new command.

    "EDIT" - Allows the user to edit an existing contact.  The 
    user will be required to enter the unique ID in order to populate the rest
    of the form with that Contact record's data.  Once populated, the user will
    have the ability modify the entire record or a specific field. If the user
    chooses to modify the entire record, they can simply not provide a new
    value if they wish for that information to remain unchanged. Their input 
    will be validated to ensure that it is of a valid data type, a proper 
    length and that all required fields have a value. After the edit has 
    completed, the user is allowed to enter a new command.

    "DELETE" - Allows the user to delete an existing contact 
    based on unique ID.  Once an ID is provided, the user will need to 
    confirm their choice to delete this Contact.  Once confirmed the Contact 
    and all its information will be deleted.  This operation is final and the
    data will not be recovered. Choosing 'No' during the confirmation will
    result in no record being deleted. Once the deletion occurs or the user
    does not confirm, the user is allowed to enter a new command.

    "IMPORT" - Allows the user to import a new data file.  Only a .txt or .csv
    file will be accepted and the contents of the file will have to be comma
    separated values.  The user will have to confirm their choice to import
    a new data file, since their current data will be overwritten.  Once the 
    import has completed, the user is allowed to enter a new command.

    "EXPORT" - This will export all contacts into a new 
    contact_list__<unix_timestamp>.csv file. The last segment of the filename 
    is a unique sequence of numbers which is also a timestamp, which will 
    allow you to create a history of your contact list files. 
    '''

    faq_str = '''
    1. My files that I import aren't working. What is the proper format?

        Answer: the proper file format is 'first_name,last_name,phone_number,
        email,company,title,relationship'. Anything additional / missing 
        fields will result in an error.  Also be careful to follow this order 
        or else your data will be out of order.    
    
    2. Why does my Unique ID value for records keep changing when I import my
        files? 

        Answer: When data is loaded, a unique ID between 1 and 1000 is assigned
        to ensure that each record has a unique identifier. This unique ID is 
        generated when the file data is imported to ensure that the IDs are 
        all of the same type and that data is not overwritten because multiple 
        of multiple records with the same id.
    '''

    print(command_descriptions)
    print("------------------------------")
    print(faq_str)

def list_contacts(contact_list:list) -> None:
    '''
        Takes in a contact_list parameter which is a list of Contact
        objects and prints them as a table for the user to view.
    '''
    # print column headers based on FIELD_NAMES tuple
    print("{:<5} {:<15} {:<15} {:<15} {:<25} {:<30} {:<30} {:<30}".format(
        FIELD_NAMES[0], FIELD_NAMES[1], FIELD_NAMES[2], FIELD_NAMES[3], 
        FIELD_NAMES[4], FIELD_NAMES[5], FIELD_NAMES[6], FIELD_NAMES[7]))

    # print separator line between headers and data
    print("{:<5} {:<15} {:<15} {:<15} {:<25} {:<30} {:<30} {:<30}"
    .format('----', '----------', '----------', '------------', 
    '----------', '----------','----------', '-------------'))
    # print all data from the contact_list
    for contact in contact_list:
        print ("{:<5} {:<15} {:<15} {:<15} {:<25} {:<30} {:<30} {:<30}"
            .format(contact.id, contact.first_name, contact.last_name, 
            contact.phone_number, contact.email, contact.company, 
            contact.title, contact.relationship ))


def add_contact(contact_list:list) -> list:
    '''
        Takes a contact_list parameter and creates a new Contact object. 
        A unique ID is created based on the current ids in the contact_list
        and the user is prompted for input for each Contact attribute.
    '''
    id_list = list()
    new_contact_values = list()
    new_contact = None

    # create list of current contact id values, then generate a new unique id
    id_list.append((c.id) for c in contact_list)
    id = generateUniqueID(id_list)

    # create list of new contact values provided by user
    new_contact_values.append(id)
    for field in FIELD_NAMES[1:]:
        value = input("{}: ".format(field))
        new_contact_values.append(value)

    # initialize new Contact instance and call the 'validate_new_contact' 
    # to validate all provided values, and ensure that this new instance
    # is unique
    new_contact = Contact(new_contact_values)
    if new_contact.is_unique(contact_list):
        new_contact.validate_new_contact()
    
    # if new_contact is not None, then add instance to contact_list
    if new_contact._Contact__is_valid:
        contact_list.append(new_contact)
        print("Successfully added new Contact!")
    else:
        messages = list(filter(None, 
            new_contact._Contact__error_message))
        print(messages)    
    return contact_list

def edit_contact(contact_list:list) -> list:
    '''
        Takes a contact_list parameter, and prompts user for an id within the 
        list. If found, the user can edit the entire record or just a single
        field. The user enters their input, which is validated, and the record
        is updated based on if it is valid or not.
    '''
    edit_contact = None
    id_found = False
    contact_list_index = 0
    input_str = str(input("Enter ID: "))
    for index,con in enumerate(contact_list):
        if(con.id == input_str):
            id_found = True
            contact_list_index = index
            # re-instantiate Contact object to prevent modifying object before
            # all validations have occurred
            edit_contact = Contact(con.__repr__().split(","))
            
            edit_instructions = '''
            Please specify what field you want to update.  If you would like
            to update the entire record, please specify the 'ALL' option.
            Providing no value for a field that already has value will not 
            update the field.
            '''
            print(edit_instructions)
            print("List of all 'EDIT' options: {}".format(
                    FIELD_NAMES[1:] + ["ALL"]))
            edit_type = input("FIELD: ").upper()

            # edit contact information based on edit_type (field or ALL)
            if edit_type == "ALL":
                # loop through all fields, except id
                for field in FIELD_NAMES[1:]:
                    print("Current Value for field {}: {}".format(edit_type, 
                        edit_contact.__dict__[field.lower()]))
                    new_value = input("New Value for field {}: ".format(field))
                    # validate that new_value is actually different from the
                    # current value and passes its field-specific validations
                    is_valid = edit_contact.validate_contact_field_update(
                        field, new_value)
                    if is_valid and new_value == "":
                        # if its valid and the new_value is empty, then keep
                        # the current value for that field.
                        pass
                    elif is_valid and new_value != "":
                        edit_contact.__dict__[field.lower()] = new_value
                    else:
                        messages = list(filter(None, 
                            edit_contact._Contact__error_message))
                        print(messages)
                        return contact_list

            elif edit_type in FIELD_NAMES:
                print("Current Value for field {}: {}".format(edit_type, 
                    edit_contact.__dict__[edit_type.lower()]))
                new_value = input("New Value for field {}: ".format(edit_type))
                # validate that new_value is actually different from the
                # current value and passes its field-specific validations
                if edit_contact.validate_contact_field_update(edit_type, 
                    new_value):
                    edit_contact.__dict__[edit_type.lower()] = new_value
                else:
                    print(edit_contact._Contact__error_message)
                    return contact_list
            else:
                print("Invalid column specified. Record not updated.")
                edit_contact = None
    
    if not id_found:
        print("Invalid ID value. No record modified")

    # Verifies that the edit_contact is not None and that it is unique from 
    # other contacts in the contact_list
    if edit_contact != None and edit_contact.is_unique(contact_list):
        contact_list[contact_list_index] = edit_contact
        print("Successfully edited Contact: {}".format(input_str))
    return contact_list
        


def delete_contact(contact_list:list) -> list:
    '''
        Takes in a contact_list parameter and prompts the user for an id in
        that list. User must confirm they want to delete the record, since 
        this action is permanent. Once confirmed, the record is deleted and
        removed from the contact_list.
    '''
    del_contact = None
    input_str = input("Enter ID: ")
    
    confirm_input = confirm("Are you sure (Yes/No): ")
    if confirm_input == "YES":

        for con in contact_list:
            if con.id == input_str:
                del_contact = con
                break
        if del_contact != None:    
            print("Successfully Deleted Contact ID: {}".format(del_contact.id))
            contact_list.remove(del_contact)
        else:
            print("Invalid ID value. No records deleted.")
    else:
        print("Contact not deleted")

    return contact_list


def import_csv_file(filepath:str) -> list:
    '''
    Import a csv file with user contacts.  
    If no file selected, then a default 'test.txt' will be loaded.
    '''
    error_txt = "ERROR: Invalid file type discovered. File extension must be: "
    contact_list = []
    extension = filepath.split(".")[1]
    if filepath != "" and os.path.isfile(filepath):
        if extension.lower() == "txt" or extension.lower() == "csv":
            contact_list = fr.read_file(filepath)
            print("LOG: Successfully loaded {} contacts!".format(
                len(contact_list)))
        else:
            print(error_txt, "{}".format(".txt or .csv"))
    else:
        # use provided test file
        print("LOG: Provided test file 'test.txt' used.")
        contact_list = fr.read_file('test.txt')
        print(error_txt, "{}".format(".txt or .csv"))

    return contact_list
    

def export_contacts(contact_list:list) -> None:
    '''
        Takes in a contact_list parameter and exports that list in the form
        of a text file where each Contact is a line with comma separated 
        values. Creates a unique filename using a unix timestamp.
    '''
    uid = int(time.time())
    export_filename = "contact_list_export__" + str(uid) + ".txt"
    file = open(export_filename, 'w')
    file.write(",".join(FIELD_NAMES))
    for item in contact_list:
        file.write("\n" + item.__repr__())
    file.close()
    print("Filename: {} created!".format(export_filename))

def generateUniqueID(id_list:list) -> str:
    '''
        Creates a random int between 1 and 1000 (arbitrary limit). 
        Then check if that id exists in the id_list parameter.
        If True, then generate new random id value
        If False, return unique id value
    '''
    is_unique = True
    # create loop to ensure a unique id is provided to every entry
    while is_unique:
        # create random ID value (int)
        randId = random.randint(1, 1000)
        # check to see if dictionary already has that key,
        # if True, then repeat loop and generate new ID
        # if False, then exit loop with unique ID
        is_unique = randId in id_list

    return str(randId)


def confirm(instructions:str) -> str:
    ''' 
        Takes in an instructions string which is used as in an input
        statement.  Recursively calls the function until the user 
        types 'yes' or 'no' (case-insensitive)
    '''
    user_input = input(instructions).upper()
    if user_input == "YES" or user_input == "NO": 
        return user_input
    else:
        return confirm(instructions) 
