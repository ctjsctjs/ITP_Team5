import pandas as pd

from config.important_attributes import attributes
from model.database import SQL
from model.dataframe import *
from controller.graph_components.regression import GraphMode

sql = SQL()
db_tables = sql.get_table_names()

# print(sql.get_attribute(db_tables[0]))

# print(sql.get_all_series())
# print(sql.get_series('DSME 11000'))


attributes = SQL().get_attributes("dsme 10700_2018_combined_a_after_dd")
print(attributes)
for key, value in attributes.items():
    print key
    print value

# options = [{'label': attribute, 'value': attribute} for attribute in attributes]
# print(options)
