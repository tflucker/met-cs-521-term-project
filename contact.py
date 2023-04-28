import string as s
import app_functions as af

class Contact(object):
    '''
       User defined class that contains basic contact information that the
       user can view, add, edit, or delete. Defines multiple class methods
       that allow for the manipulation and validation of data as it is 
       created / modified. 
    '''

    def __init__(self, line:list=None):
        '''
            Initialize new instance of the Contact class using a line (list)
            parameter.
        '''
        if line == None:
            line = [0,"","","","","","",""]
        # defining public attributes, contains information
        self.id = line[0] if not str(line[0]).isspace() else "0"
        self.first_name = line[1] if not str(line[1]).isspace() else ""
        self.last_name = line[2] if not str(line[2]).isspace() else ""
        self.phone_number = line[3] if not str(line[3]).isspace() else ""
        self.email = line[4] if not str(line[4]).isspace() else ""
        self.company = line[5] if not str(line[5]).isspace() else ""
        self.title = line[6] if not str(line[6]).isspace() else ""
        self.relationship = line[7] if not str(line[7]).isspace() else ""

        # defining private attributes, used during validation (add / edit)
        self.__is_valid = False
        self.__error_message = list()

    def __str__(self):
        '''
            Return custom string when printing a Contact class
        '''
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self) -> str:
        '''
            Return a custom string representation of the Contact class, with 
            values being returned as commas separated values.
        '''
        return "{},{},{},{},{},{},{},{}".format(self.id, self.first_name,
            self.last_name, self.phone_number,self.email, self.company, 
            self.title, self.relationship)
    
    def __eq__(self, __o: object) -> bool:
        '''
            custom implementation of the equals operator for the Contact
            class. Uses the repr method to compare comma separated strings
            (excluding the first value which is ID and is always unique)
        '''
        # getting list of values excluding id (which will always be unique)
        self_values = self.__repr__().split(',')[1:]
        other_values = __o.__repr__().split(',')[1:]
        return self_values == other_values

    def __validate_input(self, field: str, user_input: str) -> tuple:
        '''
            Validates a user_input against specific validations per field.
            If a validation fails, return a false boolean and an error message
            string.
        '''
        isValid = True
        message = ""
        # Global validation for every field
        if len(user_input) >= 30:
            isValid = False
            message = "Error: Field length must be less than 30"
        
        # Validation for FIRST NAME, LAST_NAME and RELATIONSHIP,
        # Value cannot be None or empty String
        if field in (af.FIELD_NAMES[1],af.FIELD_NAMES[2],af.FIELD_NAMES[7]):
            if user_input == "" or user_input == " " or user_input == None:
                isValid = False
                message = "Error: {} must have a value".format(field)
            
            # Validation for RELATIONSHIP
            # Value must be one of the accepted values
            if field == "RELATIONSHIP":
                accepted_values = ["FAMILY", "FRIEND", 
                    "SUPERVISOR", "COLLEAUGE", 
                    "FORMER SUPERVISOR", "FORMER COLLEAUGE"]
                if not user_input.upper() in accepted_values:
                    isValid = False
                    message = "Error: {} must be one of the ".format(field)
                    message += "following values: {}".format(accepted_values)

        # Validation for PHONE NUMBER
        # Value must follow format 'XXX-XXX-XXXX' and have a length of 12
        # using lower case comparison to check for alpha characters
        elif field == "PHONE_NUMBER":
            if (user_input.lower() != user_input) or len(user_input) != 12:
                isValid = False
                message = ("Error: {} value must follow format: {}"
                    .format(field, "XXX-XXX-XXXX"))
        
        # Validation for EMAIL
        # Value must contain an '@' and a '.' character to be considered valid
        elif field == "EMAIL":
            if not "@" in user_input or not "." in user_input:
                isValid = False
                message = "Error: Invalid format for field {}".format(field)
        else:
            pass
        
        # return tuple of bool 'isValid' and str 'message'
        return (isValid, message)

    def is_unique(self, contact_list:list) -> bool:
        '''
            Returns boolean based on if the __repr__ of the instance matches
            the __repr__ of any contact in contact_list. Equals operation 
            excludes id, since it will always be unique.
        '''
        result = True
        for c in contact_list:
            # checks contact_list to check if new instance is a duplicate
            if c.__repr__() == self.__repr__():
                result = False
        return result

    def validate_new_contact(self) -> object:
        ''' 
            If new instance is unique then validate its values. If an error is
            found, then stop validations and return 'self' object to print the 
            related error message.
        '''
        
        # if instance values unique, then validate value in each field
        for field in af.FIELD_NAMES[1:]:
            value = self.__dict__[field.lower()]
            # validate user input agains field-specific validations, two lines
            # to stay under 80 character line limit
            validation_results = tuple(self.__validate_input(field, value))
            self._Contact__is_valid = validation_results[0]
            self._Contact__error_message.append(validation_results[1])
        # if all validation passed, return Contact() instance
        return self

    def validate_contact_field_update(self,field:str,new_value:str="") -> bool:
        '''
            Takes in a field string, and a new value string for that field.
            Compare the new value agains the current value, and if value is 
            distinct, then validate the new value.  If there are errors, then
            set private variables in instance to be printed.
        '''
        result = False
        current_value = self.__dict__[field.lower()]
        if new_value == "" and current_value != "":
            # allow for the user to not provide new input, if they do not want 
            # to.  This will set the new value 
            result = True
        elif new_value != current_value:
            # validate user input agains field-specific validations
            validation_results = tuple(self.__validate_input(field, new_value))
            self._Contact__is_valid = validation_results[0]
            self._Contact__error_message.append(validation_results[1])

            # if new_value fails any validations, return 'self' object and 
            # print the related error message
            if self._Contact__is_valid:
                result = True

        else:
            self._Contact__error_message = "Duplicate value detected. "
            self._Contact__error_message += "Field not updated."

        return result