import datetime
import copy

from django.core.validators import MaxValueValidator
from django.http.request import QueryDict

from .utils import Country


class InputDataValidator:
    """
    Validator for checking required and optional fields in API input data.

    This class validates whether the input data in a request contains all the required fields 
    and optionally checks for optional fields. It is used to validate the input data in API requests.

    Attributes
    ----------
    request_data : dict
        The data from the request to validate.
    required_fields : list
        A list of required field names that must be present in the request data.
    optional_fields : list
        A list of optional field names that should be present in the request data.
    data : dict
        A dictionary to store the validated data.
    """

    def __init__(self, request,  required_fields: list=None, optional_fields: list=None) -> None:
        """
        Initialize the InputDataValidator with request data, required fields, and optional fields.

        Parameters
        ----------
        request : django.http.request.HttpRequest
            The HTTP request object containing the input data.
        required_fields : list, optional
            A list of required field names that must be present in the request data.
        optional_fields : list, optional
            A list of optional field names that should be present in the request data.
        """ 
        self.request = request
        self.request_data: dict = copy.deepcopy(request.data)
        self.required_fields = required_fields
        self.optional_fields = optional_fields
        self.data = dict()

    def check_required_fields(self):
        """
        Check if the request data contains all the required fields.

        Returns
        -------
        bool
            Returns True if all required fields are present in the request data, False otherwise.
        """
        for field in self.required_fields:
            if field not in self.request_data:
                return False
            self.data[field] = self.request_data[field]
            self.request_data.pop(field)

    def check_optional_fields(self):
        """
        Check if the request data contains all the optional fields.

        Returns
        -------
        bool
            Returns True if all optional fields are present in the request data, False otherwise.
        """
        for field in self.request.data:
            if field not in self.optional_fields:
                return False
            self.data[field] = self.request_data[field]  
            self.request_data.pop(field)

    def validate(self):
        """
        Validate the input data by checking required and optional fields.

        Returns
        -------
        bool
            Returns True if the input data contains all the required and optional fields, False otherwise.
        """
        if self.required_fields:
            self.check_required_fields()
        if self.optional_fields:
            self.check_optional_fields()
        if self.request.data != self.data:  # If no input data accepted, the self.data will be empty just as expected 
            return False
        return True


class YearValidator:
    """
    Validator for checking if a given year is valid.

    This validator checks if a given year is less than or equal to the current year.
    """
    @staticmethod
    def current_year():
        """
        Get the current year.

        Returns
        -------
        int
            The current year.
        """
        return datetime.date.today().year

    @staticmethod
    def max_year_validator(value):
        """
        Validate that the given year is less than or equal to the current year.

        Parameters
        ----------
        value : int
            The year value to validate.

        Returns
        -------
        None

        Raises
        ------
        ValidationError
            If the value is greater than the current year.
        """
        MaxValueValidator(YearValidator.current_year())(value)


class CountryValidator:
    """
    Validator for checking if a given country code is valid.

    This validator checks if a given country code is present in the list of ISO Alpha-2 country codes.
    """
    def is_valid(self, value):
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
