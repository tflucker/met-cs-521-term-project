import app_functions as af
from contact import Contact

# define global list of approved commands, displayed before asking for 
# the user input
command_list = ["LIST","ADD","EDIT","DELETE","IMPORT","EXPORT","HELP","DONE"]

def welcome_screen():
    '''
    Prints descriptive text to welcome the user, provide a brief description
    of the application, and a list of the application's functionality.
    '''

    greeting_str = '''
    Hello and welcome to the Contact List Manager application! This project 
    was developed by Timothy Flucker in November 2021 as a Final project for 
    a Python programming course.  This application is a terminal based 
    application developed in Python 3.  This project demonstates mastery of 
    basic Python syntax, logic statements, reading / writing files, functions 
    and classes.'''

    app_description = '''
    This application allows a user to import a csv file to act as the initial 
    dataset of contacts.  Once loaded, the user has the ability to 
    add / edit / delete contacts.  A new contact list file can be exported 
    at anytime.'''
    
    # print the greeting and app description doc strings to terminal
    print(greeting_str.replace("\r\n",""))
    print(app_description.replace("\r\n",""))
    print("------------------------------------------------------------")

def get_user_input():
    '''Get user input and call the corresponding function.'''
    # print commands list and then request user input
    print("\nList of approved commands (case-insensitive): ",command_list,"\n")
    return input("Command: ").upper()
  

def start_app():
    '''
    Initiates app, shows welcome text, imports default data, and invokes 
    method to get user input, relevant function called based on user input.
    '''
    welcome_screen()

    print("LOG: Loading default test file: 'test.txt' ...")
    contact_list = af.import_csv_file("test.txt")
    print("LOG: Calling 'LIST' method ... \n")
    af.list_contacts(contact_list)
    # define dictionary of functions to invoke based on key provided
    # arguments for functions defined in while loop
    command_functions = {
        "IMPORT": af.import_csv_file,
        "LIST": af.list_contacts,
        "ADD": af.add_contact,
        "EDIT": af.edit_contact,
        "DELETE": af.delete_contact,
        "EXPORT": af.export_contacts,
        "HELP": af.display_help_info
    }

    is_done = False
    while not is_done:
        # get user input
        command = get_user_input()

        # use command from user input and use it as a key in the 
        # command_functions dictionary to call a specific function
        try:
            if command == "DONE":
                is_done = True
            elif command == "HELP":
                command_functions[command]()
            elif command == "IMPORT":
                import_instructions = ''' 
                Please enter a filepath to a file you wish to import. It 
                must be a .csv or .txt file.Importing a new file
                will replace the current data with data in the new file. \n
                '''
                print(import_instructions)
                confirm_txt = "Do you still want to proceed (Yes/No)? "
                confirm_input = af.confirm(confirm_txt)
                if confirm_input == "YES":
                    custom_filepath = input("Enter path of file to import: ")
                    contact_list = command_functions[command](custom_filepath)
                else:
                    print("LOG: No file imported.")
            else:
                # if command is list, add, edit, delete, or export
                command_functions[command](contact_list)
        except KeyError:
            # if an unrecognized key provided, then return message
            print("ERROR: Command not recognized, please try again.")
        except AssertionError:
            print("ERROR: A verification for method {} has failed."
                .format(command))
        except Exception:
            print("ERROR: An error occured. Please try again.")

    # After exiting while loop print message and end application
    print("LOG: Thank you for using this application!")

if __name__ == '__main__':

    print("------------- Unit Tests (START) -------------")
    # UNIT TEST 1 - Testing Unique Check for the contact_list. Used before
    # the 'validate_new_contact' and after the 'validate_contact_field_update'
    # Contact class methods.

    # create two contacts and add to contact_list
    values1 = ["123","TimTest","PythonTest","123-456-7890","test@email.com",
        "TestCorp","Tester","Friend"]
    values2 = ["456","SallyTest","JavaTest","987-654-3210","test2@email.com",
        "TestCorp","Senior Tester","Friend"]
    c1 = Contact(values1)
    c2 = Contact(values2)
    contact_list = [c1, c2]
    # create third contact which is a duplicate 
    values3 = values1
    # This should return None because it is a duplicate
    assert not Contact(values3).is_unique(contact_list)
    print("UNIT TEST 1: contact_list unique elements check -- PASS")

    # UNIT TEST 2 - Testing 'validate_new_contact' Contact class method.
    # By adding a new Contact with unique values, the validate method should
    # return True
    values3 = ["999","MarcTest","PythonTest","123-456-7890","mtest@email.com",
        "TestCorp","Senior Tester","Supervisor"]
    assert Contact(values3).validate_new_contact()
    print("UNIT TEST 2: validate_new_contact test -- PASS")

    # UNIT TEST 3 - Testing 'validate_contact_field_update' Contact class 
    # method. By updating an existing contact with unique values, the validate 
    # method should return True
    assert Contact(values3).validate_contact_field_update("TITLE", "CEO")
    print("UNIT TEST 3: validate_contact_field_update test -- PASS")
    print("------------- Unit Tests (END) -------------")
    # call start_app method to start application
    start_app()