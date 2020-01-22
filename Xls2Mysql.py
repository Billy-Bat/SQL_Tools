# CONVERT SIMPLE EXCEL FILE TO MYSQL DATABASE

import mysql.connector as mysql

def DirectOutput(cursor, SQLCommand: str):
    cursor.execute(SQLCommand)
    output = cursor.fetchall()

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "password",
    database = "phoneNumbers"
)
cursor = db.cursor()

# Setup mySQL infrastructure
import pandas as pd
filepath = '/Users/Liam/Desktop/SQL_Tools/PhoneNumbers.xls'
headerRowID = 0 # rowIndex where the columns name are located
headersize = 1 # IN ROWS
CellRange = 'A:B' # Put None if no outlying entries (ColumnWise)

df_cols = pd.read_excel(filepath, skiprows=0, nrows=1, usecols=CellRange)
# print(df_cols.columns) # ['FIRST NAME', 'MOBILE']

# Setup The Table characteristics
table_Name = 'xlsPhoneNumbers'
PrimeKey = []
SpecialChar = {'FIRST NAME': 'NOT NULL', 'MOBILE': ''}
Types = {'FIRST NAME' : 'VARCHAR(100)', 'MOBILE' : 'VARCHAR(30)'}
AutoIncrPrimeId = True

print('WARNING: DELETING exisiting table with name "{}"'.format(table_Name))
cursor.execute('DROP TABLE IF EXISTS {}'.format(table_Name))

# Generate the Types String
TypesStr = ''
SQLColName = []
for i, col in enumerate(Types) :
    SQLColName.append(col.replace(' ', ''))
    if SpecialChar[col] :
        TypesStr += SQLColName[i] + ' ' + Types[col] + ' ' +  SpecialChar[col] + ',' + '\n'
    else :
        TypesStr += SQLColName[i] + ' ' + Types[col] + ',' + '\n'

# Generate the PrimaryKey String
if AutoIncrPrimeId & len(PrimeKey) == 0 :
    TypesStr = 'ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,\n' + TypesStr

PrimeKeyStr = ''
for key in PrimeKey :
    PrimeKeyStr += key.replace(' ', '') + ','
PrimeKeyStr = PrimeKeyStr[:-1]
if PrimeKeyStr :
    PrimeKeyStr = 'PRIMARY KEY ' + '(' + PrimeKeyStr + ')'
else :
    PrimeKeyStr = ''
    TypesStr = TypesStr[:-2]


CreateCommand = f"CREATE TABLE {table_Name} (\n{TypesStr} {PrimeKeyStr}\n);"
cursor.execute(CreateCommand)

# Populate the mySQL Table (NEED TO INCLUDE A PROPER CONVERSION BETWEEN PYTHON AND SQL DATATYPES)
df_raw = pd.read_excel(filepath, skiprows=headersize-1, names=SQLColName, dtypes=['object', 'object'], usecols=CellRange)
for row in df_raw.iterrows() :
    fields = repr(tuple(SQLColName)).replace("'", "")
    values = []
    for value in row[1]:
        values.append(str(value))
    values = tuple(values)
    # print(f'INSERT INTO {table_Name} {fields} VALUES {values};')
    cursor.execute(f'INSERT INTO {table_Name} {fields} VALUES {values};')

db.commit()
