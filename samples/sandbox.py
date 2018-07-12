import pandas as pd

from model.database import SQL
from model.dataframe import *
from controller.graph_components.regression import GraphMode

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

# for i in range(3, 10, 3):
#     print i

# for name in GraphMode:
#     print name.name

# print(GraphMode(1).name)
# print(GraphMode(1).value)

sql = SQL()
#
# print(sql.get_column_names())
# print(sql.get_vessels())
#
# print(sql.get_table_names())
#
#
# txt = "L3monade"
#
# print([unicode(txt), u'text'])

# name = "name.ext"
#
# print(name.split('.')[0])

# names = sql.get_table_names()
#
# for name in names:
#     # if '__' not in name:
#         print(name)


reading = [
    {
        u'namespace': u'dash_html_components',
        u'type': u'Div',
        u'props': {
            u'className':
                u'table-heading overflow-auto item-element-margin',
            u'children': [
                {
                    u'namespace': u'dash_html_components',
                    u'type': u'H4',
                    u'props': {
                        u'className': u'header-title panel-left',
                        u'children': u'Database Tables'
                    }
                },
                {
                    u'namespace': u'dash_html_components',
                    u'type': u'H4',
                    u'props': {
                        u'className': u'header-title panel-right',
                        u'children': u'Status'
                    }
                }
            ]
        }
    },
    {
        u'namespace': u'dash_html_components',
        u'type': u'Div',
        u'props': {
            u'className': u'table-row overflow-auto item-element-margin',
            u'children': [
                {
                    u'namespace': u'dash_html_components',
                    u'type': u'H4',
                    u'props': {
                        u'className': u'header-title panel-left',
                        u'children': u'25/08/2018, 15:34:00'
                    }
                },
                {
                    u'namespace': u'dash_html_components',
                    u'type': u'H4',
                    u'props': {
                        u'className': u'header-title panel-right',
                        u'children': u'Upload Success'
                    }
                }
            ]
        }
    },
    {
        u'namespace': u'dash_html_components',
        u'type': u'Div',
        u'props': {
            u'className': u'table-row overflow-auto item-element-margin',
            u'children': [
                {
                    u'namespace': u'dash_html_components',
                    u'type': u'H4',
                    u'props': {
                        u'className': u'header-title panel-left',
                        u'children': u'27/08/2018, 16:35:40'
                    }
                },
                {
                    u'namespace': u'dash_html_components',
                    u'type': u'H4',
                    u'props': {
                        u'className': u'header-title panel-right',
                        u'children': u'Upload Success'
                    }
                }
            ]
        }
    }
]
