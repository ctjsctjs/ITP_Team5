import pandas as pd

from config.important_attributes import attributes
from model.database import SQL
from model.dataframe import *
from controller.graph_components.regression import GraphMode

sql = SQL()
db_tables = sql.get_table_names()

# print(sql.get_attribute(db_tables[0]))

# print(sql.get_all_series())
print(sql.get_series('DSME 11000'))
