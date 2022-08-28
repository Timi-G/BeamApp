import sqlite3


def con_db(data_base):
    con = sqlite3.connect(data_base)
    return con

def com_db(con,data_base):
    cur = con.cursor()

    if cur.connection:
        con.execute('COMMIT')
    else:
        con = sqlite3.connect(data_base)
        con.execute('COMMIT')

# lines 1 to 5 can be moved to main python file
def create_databookdb(con):
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS DataBooks (DateTime text,DataBookName text,DataBookCategory text)''')

def insert_in_dbdb(con,args):
    cur = con.cursor()
    ins_db='INSERT INTO DataBooks VALUES (?,?,?)'

    if isinstance(args[0],list):
        cur.executemany(ins_db,(args))
    elif isinstance(args,list):
        cur.execute(ins_db,(args))

def select_fr_dbdb(con,dbook):
    cur = con.cursor()

    cur.execute('SELECT * FROM (?)',(dbook))
    databook=cur.fetchall()
    db=[list(row) for row in databook]
    return db

def clear_dbdb(con):
    cur = con.cursor()
    cur.execute('DELETE FROM Databooks')
#   commit changes to database

