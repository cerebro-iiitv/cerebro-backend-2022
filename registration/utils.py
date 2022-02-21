from distutils.log import error
from events.models import Event

def validate_registration_data(registration_attributes, registration_data):
    #Checking if the event require registration details

    

    if registration_attributes is not None:

        #Checking if registration details is provided
        if registration_data is None:
            error_message = {"error": "Registration data not provided"}
            return error_message

        #Checking if required details and provided details match
        if registration_data.keys() != registration_attributes.keys():
            error_message = {"error": "Invalid details provided for event registration"}
            return error_message
        
        #Iterate through each registration details and verify the input type provided
        for key in registration_data.keys():
            if registration_attributes.get(key) == "int":
                if type(registration_data.get(key)) is not int:
                        error_message = {"error": "Invalid details provided for event registration"}
                        return error_message

            elif registration_attributes.get(key) == "string":
                if type(registration_data.get(key)) is not str:
                    error_message = {"error": "Invalid details provided for event registration"}
                    return error_message

            elif registration_attributes.get(key) == "float":
                if type(registration_data.get(key)) is not float:
                    error_message = {"error": "Invalid details provided for event registration"}
                    return error_message
            
            elif registration_attributes.get(key) == "boolean":
                if type(registration_data.get(key)) is not bool:
                    error_message = {"error": "Invalid details provided for event registration"}
                    return error_message

    else:
        if registration_data is not None:
            error_message = {"error": "Registration data not required"}
            return error_message

    return None

def validate_submission_data(submission_attributes, submission_data):
    #Checking if the event require registration details


    if submission_attributes is not None:

        #Checking if registration details is provided
        if submission_data is None:
            error_message = {"error": "Submission data not provided"}
            return error_message

        #Checking if required details and provided details match
        if submission_data.keys() != submission_attributes.keys():
            error_message = {"error": "Invalid details provided for event submission"}
            return error_message
        
        #Iterate through each registration details and verify the input type provided
        for key in submission_data.keys():
            if submission_attributes.get(key) == "int":
                if type(submission_data.get(key)) is not int:
                        error_message = {"error": "Invalid details provided for event submission"}
                        return error_message

            elif submission_attributes.get(key) == "string":
                if type(submission_data.get(key)) is not str:
                    error_message = {"error": "Invalid details provided for event submission"}
                    return error_message

            elif submission_attributes.get(key) == "float":
                if type(submission_data.get(key)) is not float:
                    error_message = {"error": "Invalid details provided for event submission"}
                    return error_message
            
            elif submission_attributes.get(key) == "boolean":
                if type(submission_data.get(key)) is not bool:
                    error_message = {"error": "Invalid details provided for event submission"}
                    return error_message

    else:
        if submission_data is not None:
            error_message = {"error": "Submission data not required"}
            return error_message

    return None