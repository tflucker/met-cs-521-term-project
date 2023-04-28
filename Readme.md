# How to run Project
 1. Verify that there is a test.txt file which contains comma separated 
    values.  This will be the initial data set.
     - An alternate test file 'test2.txt' can be used to test the import
        functionality.
 2. Run the app.py class by navigating into this folder and running the command
    'python app.py' in your command prompt or IDE. This will run any unit tests
    , then import the data from the 'test.txt' file, and finally display all of 
     the data for the user.
 3. After reading the generated instructions, input any of the approved
    commands to view, create, modify, delete, or export the data.
     - the 'HELP' command will display text related to each command.
 4. Once the user is done using the project, they can input the 'DONE' 
    command and the program will thank them and end.


# Project Details
## Abstract
 This project was created by Timothy Flucker in 2021 as the final project in 
 his MET CS-521 class for his Masters of Software Development with Boston
 University. This project demonstrates mastery over the fundamentals 
 and applies them to a real world case. This project contains examples of the 
 following:
  - primitive datatypes (int, str)
  - dictionaries, lists, tuples, and sets.
  - if / else conditionals blocks
  - try / except blocks
  - creating a user-defined class with attributes and methods
  - file input and output
  - custom implementations of 'magic' methods

## Project Functionality
 1. Reading an input file to populate data.
    - There is a default file (text.txt) which will load test data 
        automatically
    - Using the 'IMPORT' functionality will allow the user to import their
        own files if they want to. This will replace any existing data in
        the application.
 2. Listing all current data as a 'prettified' string
    - This output can be obtained by inputting the 'LIST' command
 3. Adding new 'Contact' records
    - Takes in user input for all fields 
    - A unique ID value between 1 - 1000 will be generated to ensure that
        each 'Contact' has a unique identifier that can be used.
    - Checks to ensure that the data provided creates a unique record. If 
        the values provided match another record (excluding id), then no
        new 'Contact' will be created.
 4. Editing an existing 'Contact' record
    - Requires the user to specify the ID of an existing 'Contact' record.
    - The user will then type the field they wish to modify or they will 
        type 'ALL' to modify the entire 'Contact' record.
        - The user can choose not to update a field by not entering a value
            and pressing the 'Enter' button, this will default to whatever 
            the current value is for that field.
    - Checks to see if the newly updated 'Contact' record is unique. If not,
        then no record will be udpated.
 5. Deleting an existing 'Contact' record.
    - Requires the user to specify the ID of an existing 'Contact' record.
    - Prompt the user to confirm that they wish to delete this record.
        - if the user types 'YES' then the record is deleted.
        - if the user types 'NO' then the record is not deleted.
 6. Exporting the list of contacts.
    - When this command is entered, all 'Contact' records will be written
        into a 'contact_list_export__(unix-timestamp).txt' file for their
        records and future use. 
    - The unix timestamp will always be unique and allow the user to export 
        without fear of overwritting a previous export
        
## Project Organization
 - app.py: This is the main project file. 
    - contains unit tests to confirm that public class methods are working
        as intended
    - contains function that will initialize application and read in the 
        test data an list it for the user.
 - app_functions.py: The 'service' layer of the application.  Contains 
    any data translation or manipulation before interacting with the 
    'Contact' class
     - methods in this class are called using the 'my_commands' dictionary
        in the app.py class
 - csv_filereader.py: contains method to read information from a specified 
    filepath.
 - text.txt: This is the default data file which is loaded on project start.
    Contains 10 lines of data with one duplicate entry so only 9 records 
    should be created.
 - text2.txt: Another data file which is can be used to test the 'IMPORT' 
   functionality to verify that the old data is replaced with the data in
   this file.