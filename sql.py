import sqlite3
conn = sqlite3.connect('sample.db')
# conn.execute('''CREATE TABLE students 
#        (NAME TEXT  NOT NULL,
#        MARK1  TEXT  NOT NULL,
#        MARK2  TEXT  NOT NULL,
#        TOTAL  TEXT NOT NULL,
#        GRADE  TEXT);''')
conn.execute('''CREATE TABLE admin 
       (user TEXT  NOT NULL,
       pass  TEXT  NOT NULL);''')




