import re

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
        
        for key in registration_data.keys():

            if not (re.fullmatch(registration_attributes.get(key), registration_data.get(key))):
                error_message = {"error": "Invalid details provided for event registration"}
                return error_message

    else:
        if registration_data is not None:
            error_message = {"error": "Registration data not required"}
            return error_message

    return None

def validate_submission_data(submission_attributes, submission_data):
    #Checking if the event require submission details


    if submission_attributes is not None:

        #Checking if submission details is provided
        if submission_data is None:
            error_message = {"error": "Submission data not provided"}
            return error_message

        #Checking if required details and provided details match
        if submission_data.keys() != submission_attributes.keys():
            error_message = {"error": "Invalid details provided for event submission"}
            return error_message
        
        #Iterate through each submission details and verify the input type provided
        for key in submission_data.keys():
                
            if not (re.fullmatch(submission_attributes.get(key), submission_data.get(key))):
                error_message = {"error": "Invalid details provided for event submission"}
                return error_message

    else:
        if submission_data is not None:
            error_message = {"error": "Submission data not required"}
            return error_message

    return None