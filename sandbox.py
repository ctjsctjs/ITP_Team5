import pandas as pd

from model.database import SQL
from model.dataframe import DataFrame

result = SQL().get_filter_options()
df = pd.DataFrame(result)

vessel = SQL().get_vessel(vessel='AKINADA BRIDGE')

print(vessel.get_columns())
