print('Number of emails per organization')
print()
#import package
import sqlite3

# connect to database
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

#if table already exists, delete and create new one
cur.execute('''
DROP TABLE IF EXISTS Emails_per_organization''')

# create table Emails per person
cur.execute('''
CREATE TABLE Emails_per_organization (organization TEXT, count INTEGER)''')

#ask for flat file name that containes mail content
fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    # if line does not start with From, skip the line
    if not line.startswith('From: ') : continue
    
    # split the From line in pieces and select email
    pieces = line.split()
    email = pieces[1]
    parts = email.split('@')
    org = parts[-1]
    
    # count emails
    cur.execute('SELECT count FROM Emails_per_organization WHERE organization = ? ', (org, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Emails_per_organization (organization, count) 
                VALUES ( ?, 1 )''', ( org, ) )
    else : 
        cur.execute('UPDATE Emails_per_organization SET count=count+1 WHERE organization = ?', 
            (org, ))
    # This statement commits outstanding changes to disk each 
    # time through the loop - the program can be made faster 
    # by moving the commit so it runs only after the loop completes
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT organization, count FROM Emails_per_organization ORDER BY count DESC LIMIT 10'

# print all the emails per person and store it to the Emails per person
print()
print ("Counts:")
for row in cur.execute(sqlstr) :
    print (str(row[0]), row[1])

cur.close()
