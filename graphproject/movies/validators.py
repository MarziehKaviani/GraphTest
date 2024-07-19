import datetime
from django.core.validators import MaxValueValidator


class YearValidator:

    def current_year(self):
        return datetime.date.today().year


    def max_year_validator(self, value):
        return MaxValueValidator(self.current_year())(value)    
 