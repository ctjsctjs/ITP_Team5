import pandas as pd

from model.database import SQL
from model.dataframe import DataFrame

# result = SQL().get_filter_options()
# df = pd.DataFrame(result)

vessel = SQL().get_vessel(vessel='AKINADA BRIDGE')
columns = vessel.get_columns()

# print("------------------------------------------------------")
# for i in range(len(columns)):
#     print("%d: %s" % (i, columns[i]))
# print("------------------------------------------------------")
#
# data = vessel.get_2D_data(columns[12], columns[183], clean=True)
#
# conditions = [
#     (columns[12], "==", "Berth"),
#     (columns[12], "==", "Sea", ),
# ]
#
# print(vessel.get_2D_data(columns[10], columns[183], conditions))
vessel.get_filtered()
print(SQL().get_column_datatypes(column="Mode Code", singular=True))
