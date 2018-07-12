from config.important_attributes import attributes
from model.database import SQL


col_no = [
    0,  # 0. Draft
    0,  # 1. Weather
    0,  # 2. Sea State
    0,  # 3. Swell
    10,  # 4. Speed
    14,  # 5. RPM
    34,  # 6. Trim
    0,  # 7. Power
]


# Display column names with index no.
def get_names(names):
    for name in names:
        print "{}. {}".format(names.index(name), name)


sql = SQL()

# # Read Attributes
# get_names(attributes)

# Get database tables
db_tables = sql.get_table_names()
# get_names(db_tables)

# Get column names for given database
column_names = sql.get_column_names(db_tables[0])
# get_names(column_names)

# Insert Speed
for i in range(len(col_no)):
    if col_no[i] > 0:
        sql.set_attribute(
            db_table=db_tables[0],
            column_name=column_names[col_no[i]],
            attribute=attributes[i]
        )
