import datetime
from django.core.validators import MaxValueValidator
from django.http.request import QueryDict

from .utils import Country


class InputDataValidator:
    def __init__(self, request,  required_fields: list=None, optional_fields: list=None) -> None:
        self.request_data: dict = request.data
        self.required_fields = required_fields
        self.optional_fields = optional_fields
        self.data = dict()

    def check_required_fields(self):
        for field in self.required_fields:
            if field not in self.request_data:
                return False
            self.request_data.pop(field)
            self.data[field] = self.request_data[field]

    def check_optional_fields(self):
        for field in self.optional_fields:
            if field not in self.request_data:
                return False
            self.request_data.pop(field)
            self.data[field] = self.request_data[field]  

    def validate(self):
        if self.required_fields:
            self.check_required_fields()
        if self.optional_fields:
            self.check_optional_fields()
        if self.request_data != self.data:  # If no input data accepted, the self.data will be empty just as expected 
            return False
        return True

def check_api_input_data(request, required_fields):
    """
    Check if the API input data contains the required and optional fields.

    This function checks whether the input data in the request contains all the
    required fields and optionally checks for optional fields. It is used to
    validate the input data in API requests.

    Parameters
    ----------
    request : django.http.request.HttpRequest
        The HTTP request object containing the input data.
    required_fields : list
        A list of required field names that must be present in the request data.
    Returns
    -------
    bool
        Returns True if the input data contains all the required and optional fields,
        False otherwise.
    """
    data = dict()
    request_data = request.data
    if required_fields:
        for field in required_fields:
            if field not in request_data:
                return False
            data[field] = request_data[field]
    if type(request_data) == QueryDict:  # Type of data in django tests, is querydict
        request_data = request_data.dict()
    return data == request_data


class YearValidator:
    """
    Validator for checking if a given year is valid.

    This validator checks if a given year is less than or equal to the current year.
    """
    def current_year(self):
        """
        Get the current year.

        Returns
        -------
        int
            The current year.
        """
        return datetime.date.today().year

    def max_year_validator(self, value):
        """
        Validate that the given year is less than or equal to the current year.

        Parameters
        ----------
        value : int
            The year value to validate.

        Returns
        -------
        django.core.validators.MaxValueValidator
            A MaxValueValidator instance configured to validate the given year.
        """
        return MaxValueValidator(self.current_year())(value)    
 

class CountryValidator:
    """
    Validator for checking if a given country code is valid.

    This validator checks if a given country code is present in the list of ISO Alpha-2 country codes.
    """
    def is_valid(value):
        """
        Validate if the given country code is valid.

        Parameters
        ----------
        value : str
            The country code to validate.

        Returns
        -------
        bool
            Returns True if the country code is valid, False otherwise.
        """
        return str(value).strip() in Country().IsoAlpha2List
