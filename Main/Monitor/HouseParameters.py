import sqlite3 as sql
from DBFunc import DBInit, DBInsert, DBCommit
import pandas as pd

def GetHouseParams(path:str, houseID: int)->tuple[tuple, str]:
    try: 
        con, error = DBInit(path)
        if error:
            return None, error

        query = """ SELECT * FROM HouseConfig
                    WHERE HOUSEID = ?"""
        cursor = con.cursor()

        cursor.execute(query, (houseID,))
        params = cursor.fetchone()
        
        return params, None

    except sql.Error as error:
        return None, error.__str__()
    
def SetHouseParams(path: str, houseID: int, params: tuple)->str:
    if params.__len__() != 6:
        return f"Params of len {params.__len__()}. Must be 6"
    
    try:
        con = sql.Connection(path)
        query = """UPDATE HouseConfig SET
                    TEMPMIN = ?,
                    TEMPMAX = ?,
                    HUMDMIN = ?,
                    HUMDMAX = ?,
                    MOISTMIN = ?,
                    MOISTMAX = ?
                    WHERE HOUSEID = ?;"""
        
        con.execute(query, params + (houseID,))
        con.commit()
        con.close()
        return f"House {houseID} params updated successfully in DB"
    
    except sql.Error as error:
        return error.__str__()
        


if __name__ == "__main__":
    path = "Main\\Monitor\\test.db"

    params, error = GetHouseParams(path, 1)
    if (error):
        print(error)
    else:
        print(params)

    print(SetHouseParams(path, 2, (20.5, 30.5, 30.6, 70.6, 20.5, 40.6)))

    params, error = GetHouseParams(path, 2)

    if(error):
        print(error)
    else:
        print(params)

    # con, error = DBInit(path)

    # if error:
    #     print(error)
    #     exit()

    # con.execute("""
    #             CREATE TABLE IF NOT EXISTS HouseConfig(
    #             HOUSEID INTEGER,
    #             TEMPMIN INTEGER,
    #             TEMPMAX INTEGER,
    #             HUMDMIN INTEGER,
    #             HUMDMAX INTEGER,
    #             MOISTMIN INTEGER,
    #             MOISTMAX INTEGER);
    #             """)
    
    # query: str = """UPDATE HouseConfig SET
    #                 TEMPMIN = ?,
    #                 TEMPMAX = ?,
    #                 HUMDMIN = ?,
    #                 HUMDMAX = ?,
    #                 MOISTMIN = ?,
    #                 MOISTMAX = ?
    #                 WHERE HOUSEID = ?;"""
    # success, error = DBInsert(con, query, (20.5, 30.5, 20.0, 60.0, 10.3, 30.7, 1))
    # if (error):
    #     print(error)
    # success, error = DBInsert(con, query, (22.5, 35.5, 21.0, 65.0, 11.3, 35.7, 2))
    # if (error):
    #     print(error)
    # success, error = DBInsert(con, query, (21.5, 33.5, 30.0, 50.4, 12.3, 25.7, 3))
    # if (error):
    #     print(error)
    # success, error = DBInsert(con, query, (19.5, 31.5, 22.0, 53.0, 14.3, 36.7, 4))
    # if (error):
    #     print(error)
    # success, error = DBInsert(con, query, (10.5, 35.5, 21.0, 45.0, 12.3, 34.7, 5))
    # if (error):
    #     print(error)

    # success, error = DBCommit(con)

    # con.close()
    