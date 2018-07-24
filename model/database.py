from pymysql import connect, Error
import pandas as pd

import config.database_settings as dbconf
from model.dataframe import *


class SQL:
    def __init__(self, host=dbconf.host, user=dbconf.user, password=dbconf.password, db=dbconf.db, port=dbconf.port,
                 encoding=dbconf.encoding):
        # Connection Settings
        self.__host = host
        self.__user = user
        self.__password = password
        self.__db = db
        self.__port = port

        self.__connection = None
        self.__cursor = None
        self.__encoding = encoding
        self.__filter_limit = 100
        # FOR TESTING/DEBUGGING TODO:remove when deemed unnecessary
        self.__default_table = "dsme 10700_2018_combined_a_after_dd"

    def __del__(self):
        self.__close()

    def destroy(self):
        self.__del__()

    def get_table(self, table=None):
        if table is None:
            return None

        query = "SELECT * FROM `" + table + "`"

        self.__reconnect()
        return pd.read_sql(sql=query, con=self.__connection)

    """
    'Graph Parameters' Methods
    """

    # Method to obtain all column names in a table
    def get_column_names(self, table=None):
        # TODO: # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # Get Column Names from Database
        result = self.__select(columns="COLUMN_NAME", table="INFORMATION_SCHEMA.COLUMNS",
                               condition={'table_name': table})

        # Clean Data before returning
        column_names = []
        for name in result:
            column_names.append(name[0])

        # Return Data
        return column_names

    # Method to obtain the datatype and size of each column in a table
    def get_column_datatypes(self, table=None, distinct=False, column=None, singular=False):
        # TODO: Invalid argument handling
        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        if singular and column is not None:
            # Get Column datatypes from Database TODO: Use SQL 'DISTINCT'
            condition = {'table_name': '{}'.format(table), 'column_name': '{}'.format(column)}
            result = self.__select(columns="DATA_TYPE", table="INFORMATION_SCHEMA.COLUMNS", condition=condition)

            # Clean and Return Data
            return result[0][0]
        else:
            # Get Column datatypes from Database TODO: Use SQL 'DISTINCT'
            condition = {'table_name': '{}'.format(table)}
            result = self.__select(columns="DATA_TYPE, CHARACTER_MAXIMUM_LENGTH", table="INFORMATION_SCHEMA.COLUMNS",
                                   condition=condition)

            # Clean Data before returning
            column_datatypes = []
            for col_name, col_type in result:
                column_datatypes.append([col_name, col_type])

            # Return Data
            if distinct:
                return [list(x) for x in set(tuple(x) for x in column_datatypes)]
            return column_datatypes

    # Method to obtain filter options
    def get_filter_options(self, table=None):
        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # Get Column Info from Database TODO: Use SQL 'DISTINCT'
        condition = {'table_name': '{}'.format(table)}
        info = self.__select(columns="COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH",
                             table="INFORMATION_SCHEMA.COLUMNS", condition=condition)

        # Filter
        filtered_info = []
        for item in info:
            if item[2] <= self.__filter_limit:
                filtered_info.append(item)

        return filtered_info

    """
    'Vessel' Methods
    """

    # Obtain all existing series
    def get_all_series(self):
        all_series = self.__select(
            columns="Series",
            table="__series",
            distinct=True
        )

        return [series[0] for series in all_series]

    # Obtain Vessel names within a given series
    def get_series(self, series):
        vessels = self.__select(
            columns="Vessel",
            table="__series",
            condition={'Series': '{}'.format(series)}
        )

        return [vessel[0] for vessel in vessels]

    # Method to obtain distinct vessel codes/names TODO: Too reliant on hardcode. Possible redesign required
    def get_vessels(self, table=None, column=None):
        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # TODO: Better handle 'No column given' condition
        if column is None:
            column = 'Vessel'
            # column = 'DISTINCT `Vessel Code`'

        result = self.__select(table=table, columns=column, distinct=True)
        if result is not None:
            clean_result = []
            for i in result:
                if i[0] is not None:
                    clean_result.append(i[0])
            return clean_result
        return

    # Method to obtain data for a particular vessel
    def get_vessel(self, table=None, vessel=None):
        # TODO: # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # TODO: Handle 'No vessel given' event
        if vessel is None:
            return

        self.__reconnect()
        # TODO: Stop using pd
        # TODO: Remvoe hardcoded 'vessel' name
        df = pd.read_sql(sql="SELECT * FROM `{}` WHERE `Vessel`='{}'".format(table, vessel), con=self.__connection)
        return DataFrame(df)

    # Method to obtain data of all vessels in series
    def get_df_from_series(self, table=None, series=None):
        # TODO: # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # TODO: Handle 'No vessel given' event
        if series is None:
            return

        self.__reconnect()
        # TODO: Stop using pd
        # TODO: Remvoe hardcoded 'vessel' name
        df = pd.read_sql(sql="SELECT * FROM `{}` WHERE `Vessel` IN (SELECT `Vessel` FROM `vessel_series` WHERE `Series` = '{}')".format(table, series), con=self.__connection)
        return df

    # Method to obtain vessel short forms
    def get_vessel_shortform(self):
        self.__reconnect()
        sql = "SELECT * FROM `vesselshortform`"
        results = self.__query(sql, expect_result=True)
        sfList = {}
        if results is not None:
            for result in results:
                sfList[result[2]] = result[1]
        return sfList

    # Method to obtain all distinct vessels in a given table from a given series
    def get_vessel_from_series(self, series, db_table):
        vessels_in_series = self.get_series('{}'.format(series))
        vessels_in_table = self.get_vessels(table=db_table)

        vessels = []
        for vessel in vessels_in_table:
            if vessel in vessels_in_series:
                vessels.append(vessel)

        if len(vessels) > 0:
            return vessels
        return

    """
    'Database' Methods
    """

    # Obtain table names from database
    def get_table_names(self):
        # Obtain table names
        table_names = self.__select(columns="TABLE_NAME", table="INFORMATION_SCHEMA.TABLES",
                                    condition={'TABLE_TYPE': 'BASE TABLE', 'TABLE_SCHEMA': self.__db})

        return [table[0] for table in table_names if '__' not in table[0]]

    # Excel-to-SQL Function
    def excel_to_sql(self, table_name, excel_file, filetype=FileType.OTHERS):
        # TODO: Get sheet number
        df = DataFrame(excel_file, filetype)
        columns = df.get_columns()

        # Create empty table in database
        self.__create(table=table_name, columns=columns, datatype=df.get_column_datatypes())

        # Instantiate results
        result = {'pass': 0, 'fail': 0, 'failed_rows': []}

        # Populate table with xlsx data
        for i in range(df.len()):
            row = df.get_row(i + 1)

            col = ""
            val = ""
            valid_rows = len(columns)

            for j in range(len(columns) - 1, -1, -1):
                if not pd.isnull(row[j]):
                    break
                valid_rows -= 1

            for j in range(valid_rows):
                if not pd.isnull(row[j]):
                    col += "`" + columns[j] + "`"
                    val += '"' + unicode(row[j]).replace('"', '\\"') + '"'

                    if j is not (valid_rows - 1):
                        col += ","
                        val += ","

            insert_query = "INSERT INTO `" + table_name + "` (" + col + ") VALUES (" + val + ")"

            # err = self.__query(insert_query)
            # if err is not None:
            #     print(err)

            if self.__query(insert_query):
                result['pass'] += 1
            else:
                result['fail'] += 1
                result['failed_rows'].append(i)

        return result

    # Delete given db table
    def delete_table(self, table):
        if table is not None:
            return self.__drop(table)

    # Get number of rows in given table
    def get_table_rows(self, table):
        result = self.__select(columns="COUNT(*)", table=table)
        if result is not None:
            return result[0][0]

    """
    'Important Attributes' Methods
    """

    # Obtain existing attributes from a given table
    def get_attributes(self, db_table):
        attributes = self.__select(
            columns="attribute, column_name",
            table="__important_attributes",
            condition={'db_table': '{}'.format(db_table)}
        )

        return {"{}".format(key): "{}".format(value) for key, value in attributes}

    # Add/Update an attribute
    def set_attribute(self, db_table, column_name, attribute):
        # Check if attribute exists
        if (len(self.__select(table="__important_attributes",
                              condition={'db_table': '{}'.format(db_table), 'attribute': '{}'.format(attribute)})) > 0):
            self.__update(
                table="__important_attributes",
                changes={'column_name': column_name},
                condition={'db_table': db_table, 'attribute': attribute})
        else:
            self.__insert(
                columns=['db_table', 'column_name', 'attribute'],
                table="__important_attributes",
                data=[db_table, column_name, attribute]
            )

    """
    Base Methods
    """

    # Craft conditions for SQL Queries. Takes dictionaries eg. {'column': 'value'}
    def __condition(self, condition):
        con = ""
        for key, value in condition.items():
            con += "`{}`='{}'".format(key, value)
            if key is not condition.keys()[-1]:
                con += " AND "

        return con

    # SQL Select Method
    def __select(self, columns="*", table=None, condition=None, distinct=False):
        # TODO: Handle 404
        # TODO: Craft format for conditions
        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table
        elif not table.__contains__('INFORMATION_SCHEMA'):
            table = '`{}`'.format(table)

        if distinct:
            sql = "SELECT DISTINCT {} FROM {}".format(columns, table)
        # Construct SELECT Query
        else:
            sql = "SELECT {} FROM {}".format(columns, table)

        # If condition given
        if condition is not None:
            sql += " WHERE " + self.__condition(condition)

        # Run Query
        return self.__query(sql, expect_result=True)
        # self.__reconnect()
        # return pd.read_sql(sql=sql, con=self.__connection)

    # SQL Insert Method
    def __insert(self, columns=[], table=None, data=[]):
        # TODO: Handle error where 'columns' and 'data' do not match(i.e different number of elements)
        # TODO: Handle event where 'row' already exists in Database(i.e Replace or Combine?)

        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # Construct INSERT Query
        sql_columns = ""
        sql_data = ""
        for i in range(len(columns)):
            if i is not 0:
                sql_columns += ","
                sql_data += ","

            sql_columns += columns[i]
            sql_data += '"' + unicode(str(data[i])).replace('"', '\\"') + '"'

        sql = "INSERT INTO `" + table + "`(" + sql_columns + ") VALUES (" + sql_data + ")"
        # Run Query
        self.__query(statement=sql, expect_result=False)

    # SQL Update Table Method
    def __update(self, table, changes={}, condition={}):
        # Craft 'SET' field
        set_field = ""
        for key, value in changes.items():
            set_field += "`{}`='{}'".format(key, value)
            if key is not changes.keys()[-1]:
                set_field += ", "

        return self.__query("UPDATE `{}` SET {} WHERE {}".format(table, set_field, self.__condition(condition)))

    # SQL Create Table Method
    def __create(self, table=None, columns=[], datatype=[]):
        # TODO: Handle invalid arguments(i.e 'id' in 'columns')
        # TODO: Handle error where 'columns' and 'data' do not match(i.e different number of elements)
        # TODO: Handle event where 'table' already exists in Database(i.e Replace or Combine?). Currently replacing

        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # Drop table if it already exist in Database
        sql_drop = "DROP TABLE IF EXISTS `" + table + "`"
        self.__query(sql_drop)

        # First part of query, with 'id' as an auto incrementing index
        sql = "CREATE TABLE `" + table + "` (`id` int(11) NOT NULL AUTO_INCREMENT,"

        # Add each column name with its data type to statement
        for i in range(len(columns)):
            line = "`" + columns[i] + "`"

            # Check data type of column and add accordingly TODO: Reconsider hardcoded data sizes
            if datatype[i] == 'datetime64[ns]':
                line += " DATETIME"
            elif datatype[i] == 'object':
                if "Remarks" in columns[i] or "Reason" in columns[i]:
                    line += " VARCHAR(512)"
                elif "Email" in columns[i]:
                    line += " VARCHAR(100)"
                else:
                    line += " VARCHAR(50)"
            elif datatype[i] == 'int64':
                line += " INT"
            elif datatype[i] == 'float64':
                line += " FLOAT"

            # Include comma and add portion to query
            line += ","
            sql += line

        # End part of query
        sql += "PRIMARY KEY (`id`)) ENGINE=InnoDB CHARACTER SET utf8 COLLATE utf8_bin"

        # Run Query
        return self.__query(sql)

    # SQL Drop Table Method
    def __drop(self, table):
        return self.__query(statement="DROP TABLE `{}`".format(table))

    # Basic Query Function
    def __query(self, statement, expect_result=False):
        self.__reconnect()
        result = True
        try:
            with self.__cursor as cursor:
                # Run SQL Query
                cursor.execute(statement.encode(self.__encoding))
                self.__connection.commit()

                # If result is expected
                if expect_result:
                    result = cursor.fetchall()
            return result
        except Error as e:
            # print("Error %d: %s" % (e.args[0], e.args[1]))
            return False

    # Open Connection Method
    def __reconnect(self):
        self.__close()

        self.__connection = connect(host=self.__host, user=self.__user, password=self.__password, db=self.__db,
                                    port=self.__port)
        self.__cursor = self.__connection.cursor()

    # Close Connection Method
    def __close(self):
        if self.__connection is not None:
            self.__connection.close()
