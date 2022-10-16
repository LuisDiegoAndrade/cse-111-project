'''
This script tests executing raw SQL statements in SQLAlchemy.
We take advantage of SQLAlchemy's structuring of the queries, but we strictly only use raw query statements for the sake of the course and its goals.
'''

'''
Data comes from Kaggle.com
'''

import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

#Change this path when running on your system if needed. Database is in the current working directory.
engine = sqlalchemy.create_engine('sqlite:///cve')
Session = scoped_session(sessionmaker(bind=engine))

s = Session()

# run query against 'cve-vendors-products' table that returns all rows where the vendor
## is google

# Escape "-" character in table name by wrapping table name in back ticks
result = s.execute('SELECT * FROM `cveitems` WHERE ROWID = :val', {'val': 2})
# iterate through results
for item in result:
    print(item)

print() # newline

result = s.execute('SELECT * FROM `cve-vendors-products` WHERE ROWID = :val', {'val': 2})

# iterate through results
for item in result:
    print(item)
