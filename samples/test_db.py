from sqlalchemy import create_engine
import pandas as pd


class ENGINE:
    def __init__(self):
        self.ENGINE = create_engine('sqlite:///sample.db')
        self.create_sample_database()

    # Create a simple database
    def create_sample_database(self):
        df = pd.DataFrame({
            'column_a': [1, 2, 3, 4, 5, 6],
            'column_b': [6, 5, 4, 3, 2, 1],
            'column_c': ['a', 'b', 'c', 'a', 'a', 'b']
        })
        df.to_sql('dataframe', self.ENGINE, if_exists='replace')
