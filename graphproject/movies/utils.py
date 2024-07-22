import pandas as pd
from django.conf import settings

countries = None
countries_choices = None


class Country:
    """
    A class to handle country data, including loading country information from a CSV file
    and providing country choices for use in forms or other applications.

    Attributes
    ----------
    countries_df : pd.DataFrame
        A DataFrame containing the country data.
    IsoAlpha2List : list
        A list of ISO Alpha-2 country codes.
    countries_choices : list
        A list of tuples containing ISO Alpha-2 codes and country names.

    Methods
    -------
    load_countries_lazy() -> pd.DataFrame
        Loads the country data from a CSV file if not already loaded.
    get_choices() -> list
        Returns a list of tuples containing ISO Alpha-2 codes and country names.
    """

    def __init__(self) -> None:
        """
        Initializes the Country instance by loading country data and preparing
        the ISO Alpha-2 code list.
        """
        self.countries_df: pd.DataFrame = self.load_countries_lazy()
        self.IsoAlpha2List = self.countries_df['IsoAlpha2'].to_list()

    def load_countries_lazy(self):
        """
        Loads country data from a CSV file if it is not already loaded.

        The CSV file is located in the 'assets' directory of the Django project.
        The method filters the DataFrame to include only independent countries and
        adjusts specific country codes (e.g., Namibia).

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the filtered country data with columns 'Name' and 'IsoAlpha2'.
        """
        global countries
        if not isinstance(countries, pd.DataFrame):
            df = pd.read_csv(f'{settings.BASE_DIR}/assets/country_data.csv')
            df = df[df['isIndependent'] == 'Yes'][['Name', "IsoAlpha2"]]
            df.loc[df['Name'] == 'Namibia', 'IsoAlpha2'] = 'NA'
            countries = df
        return countries

    def get_choices(self):
        """
        Generates a list of tuples containing ISO Alpha-2 codes and country names.

        Returns
        -------
        list
            A list of tuples where each tuple contains an ISO Alpha-2 code and the corresponding country name.
        """
        global countries_choices
        if not countries_choices:
            countries_choices = [(row['IsoAlpha2'], row['Name'])
                                 for _, row in self.countries_df.iterrows()]
        return countries_choices
