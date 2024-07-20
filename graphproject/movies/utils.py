import pandas as pd
from django.conf import settings

countries = None
countries_choices = None


class Country:

    def __init__(self) -> None:
        self.countries_df: pd.DataFrame = self.load_countries_lazy()
        self.IsoAlpha2List = self.countries_df['IsoAlpha2'].to_list()

    def load_countries_lazy(self):
        global countries 
        if not countries:
            df = pd.read_csv(f'{settings.BASE_DIR}/assets/country_data.csv')
            df = df[df['isIndependent'] == 'Yes'][['Name', "IsoAlpha2"]]
            df.loc[df['Name'] == 'Namibia', 'IsoAlpha2'] = 'NA'
            countries = df
        return countries 
    
    def get_choices(self):
        global countries_choices
        if not countries_choices:
            countries_choices = [(row['IsoAlpha2'], row['Name']) for _, row in self.countries_df.iterrows()]
        return countries_choices
    

