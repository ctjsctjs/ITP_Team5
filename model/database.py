import pymysql
import pandas as pd
import config.database_settings as dbconf


class SQL:
    def __init__(self, host=dbconf.host, user=dbconf.user, password=dbconf.password, db=dbconf.db,
                 encoding=dbconf.encoding):
        # Connection Settings
        self.__host = host
        self.__user = user
        self.__password = password
        self.__db = db

        self.__connection = None
        self.__cursor = None
        self.__encoding = encoding

        # FOR TESTING/DEBUGGING TODO:remove when deemed unnecessary
        self.__default_table = "table_1"

    def __del__(self):
        self.__close()

    def destroy(self):
        self.__del__()

    # FOR TESTING/DEBUGGING TODO:remove when deemed unnecessary
    def test(self):
        self.__reconnect()
        frame = pd.read_sql(sql="SELECT * FROM vomsii_data WHERE `Vessel Code`='AJIAPL'", con=self.__connection)
        return frame

    # FOR TESTING/DEBUGGING TODO:remove when deemed unnecessary
    def connection(self):
        return self.__connection

    def get_column_names(self, table=None):
        if table is None:
            table = self.__default_table

        # Get Column Names from Database
        condition = "table_name = '" + table + "'"
        result = self.select(columns="COLUMN_NAME", table="INFORMATION_SCHEMA.COLUMNS", condition=condition)

        # Clean Data before returning
        column_names = []
        for name in result:
            column_names.append(name[0])

        # Return Data
        return column_names

    def get_table(self, table=None):
        if table is None:
            return None

        query = "SELECT * FROM `" + table + "`"

        self.__reconnect()
        return pd.read_sql(sql=query, con=self.__connection)

    # SQL Create Table Method
    def create(self, table=None, columns=[], datatype=[]):
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

            # Check data type of column and add accordingly
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
        self.__query(sql)

    # SQL Select Method
    def select(self, columns="*", table=None, condition=None):
        # TODO: Handle 404

        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # Construct SELECT Query
        sql = "SELECT " + columns + " FROM " + table

        # If condition given
        if condition is not None:
            sql += " WHERE " + condition
            print(False)

        # Run Query
        return self.__query(sql, expect_result=True)
        # self.__reconnect()
        # return pd.read_sql(sql=sql, con=self.__connection)

    # SQL Insert Method
    def insert(self, columns=[], table=None, data=[]):
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

    # FOR TESTING/DEBUGGING TODO:remove when deemed unnecessary
    def query(self, statement, expect_result=False):
        return self.__query(statement, expect_result)

    # Basic Query Function
    def __query(self, statement, expect_result=False):
        self.__reconnect()

        result = None
        print(statement)
        try:
            with self.__cursor as cursor:
                # Run SQL Query
                cursor.execute(statement.encode(self.__encoding))
                self.__connection.commit()

                # If result is expected
                if expect_result:
                    result = cursor.fetchall()
        finally:
            return result

    # Open Connection Method
    def __reconnect(self):
        self.__close()

        self.__connection = pymysql.connect(host=self.__host, user=self.__user, password=self.__password, db=self.__db)
        self.__cursor = self.__connection.cursor()

    # Close Connection Method
    def __close(self):
        if self.__connection is not None:
            self.__connection.close()
