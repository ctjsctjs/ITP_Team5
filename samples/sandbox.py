import pandas as pd

from model.database import SQL
from model.dataframe import DataFrame


# result = SQL().get_filter_options()
# df = pd.DataFrame(result)

# vessel = SQL().get_vessel(vessel='AKINADA BRIDGE')
# columns = vessel.get_columns()
#
# print("------------------------------------------------------")
# for i in range(len(columns)):
#     print("%d: %s" % (i, columns[i]))
# print("------------------------------------------------------")
#
# data = vessel.get_2D_data(columns[12], columns[183], clean=True)
#
# conditions = [
#     (columns[12], "==", "'Berth'"),
#     (columns[12], "==", "'Sea'"),
#     (columns[4], "<", 100),
# ]
#
# df = vessel.get_df()
# # print(df[df["Voyage Nbr"] <= 100])
# print(vessel.get_2D_data(columns[12], columns[183], conditions))

# print(vessel.get_filtered(conditions))
# print(SQL().get_column_datatypes(column="Mode Code", singular=True))

# print(SQL().get_column_datatypes(column='Vessel Code', singular=True))


# def func(*args):
#     for item in args:
#         print(args)
#
# func(1,2,3)

for i in range(3, 10, 3):
    print i
