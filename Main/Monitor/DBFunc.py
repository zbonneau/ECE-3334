import sqlite3 as sql


def DBInit(path:str)->sql.Connection:
    try:
        con = sql.connect(path)
        return con
    except sql.Error as error:
        return None
    
def DBClose(con:sql.Connection)->bool:
    try:
        con.close()
        return True
    except sql.Error as error:
        return False
    
def DBInsert(con:sql.Connection, query:str, params:tuple[any])->bool:
    try:
        con.execute(query, params)
        con.commit()
        return True
    except sql.Error as error:
        return False
    
def main():
    path:str = "Main\\Monitor\\test.db"

    con:sql.Connection = DBInit(path)

    if con is None:
        print("Failed to connect")
        return
    
    con.execute("""CREATE TABLE IF NOT EXISTS func(
                DATETIME TEXT,
                HOUSE INTEGER,
                TEMP REAL,
                HUMIDITY REAL,
                MOISTURE REAL);""")
    
    while(1):
        entry: str = input("Give entry (D,Hs,T,Hm,M): ")

        if (entry == 'q'):
            break

        params:tuple[any] = entry.split(' ')
        if (params.__len__() != 5):
            print("Bad params")
            continue

        fparams = (params[0],
                (int)(params[1]), 
                (float)(params[2]), 
                (float)(params[3]), 
                (float)(params[4]))
        
        query:str = """INSERT INTO func VALUES(?,?,?,?,?);"""
        if not DBInsert(con,query,fparams):
            print("insert failed")
        

    DBClose(con)


if __name__ == "__main__":
    main()