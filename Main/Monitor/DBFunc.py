import sqlite3 as sql


def DBInit(path:str)->tuple[sql.Connection,str]:
    try:
        con = sql.connect(path)
        return (con, None)
    except sql.Error as error:
        return (None, error.__str__)
    
def DBClose(con:sql.Connection)->tuple[bool,str]:
    try:
        con.close()
        return True, None
    except sql.Error as error:
        return (False, error.__str__())
    
def DBInsert(con:sql.Connection, query:str, params:tuple[any])->tuple[bool,str]:
    try:
        con.execute(query, params)
        return (True,None)
    except sql.Error as error:
        return (False, error.__str__())

def DBCommit(con:sql.Connection)->tuple[bool, str]:
    try:
        con.commit()
        return (True, None)
    except sql.Error as error:
        return (False, error.__str__())

def stringParse(string: str, args:int)->tuple[any]:
    split = string.split(",")

    if (split.__len__() != args):
        return None
    
    params = (
        split[0],
        (int)(split[1]),
        (float)(split[2]),
        (float)(split[3]),
        (float)(split[4])
    )

    return params

    
def main():
    path:str = "Main\\Monitor\\test.db"

    con, error = DBInit(path)

    if con is None:
        print(error)
        return
    
    con.execute("""CREATE TABLE IF NOT EXISTS func(
                DATETIME TEXT,
                HOUSE INTEGER,
                TEMP REAL,
                HUMIDITY REAL,
                MOISTURE REAL);""")
    
    query:str = """INSERT INTO func VALUES(?,?,?,?,?);"""
    while(1):
        entry: str = input("Give entry (D,Hs,T,Hm,M): ")

        if (entry == 'q'):
            break

        if (entry == 'c'):
            success, error = DBCommit(con)
            if (not success):
                print(error)
            continue

        fparams = stringParse(entry, 5)
        if not fparams:
            print("Bad Message ->",entry)
            continue
        success, error = DBInsert(con,query,fparams)
        if not success:
            print(error)
        

    DBClose(con)


if __name__ == "__main__":
    main()