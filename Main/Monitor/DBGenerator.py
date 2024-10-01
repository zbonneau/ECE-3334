import sqlite3 as sql
from datetime import datetime
from datetime import timedelta
from random import random, randint

def generate(con:sql.Connection, entries: int)->None:
    query = """INSERT INTO example VALUES(?,?,?,?,?);"""
    try:
            
        for _ in range(entries):
                dateRand = datetime(randint(2020, 2025), randint(1,12),randint(1,28), randint(0,23), randint(0,59))
                queryDT = dateRand.isoformat(sep=" ", timespec="minutes")
                House = randint(1,5)
                Temp  = round(random() * 20 + 20, 2)
                Humd  = round(random() * 5, 2)
                Moist = round(random() * 15 + 5, 2)

                params = (queryDT, House, Temp, Humd, Moist)
                con.execute(query, params)
            
        return

    except sql.Error as error:
        return
    
def generateSequence(con:sql.Connection, entries:int)->None:
    query = """INSERT INTO example VALUES(?,?,?,?,?);"""
    date = datetime.now()
    Temp  = round(random() + 25, 2)
    Humd  = round(random() + 20, 2)
    Moist = round(random() + 30, 2)
    
    try:
        for _ in range(entries):
            date += timedelta(minutes=15)
            queryDT = date.isoformat(sep=" ", timespec="minutes")
            House = randint(1,5)
            Temp  = max(20,min(40, Temp  + round(random()-0.5,2)))
            Humd  = max(15,min(80, Humd  + round(random()-0.5,2)))
            Moist = max(10,min(60, Moist + round(random()-0.5,2)))

            params = (queryDT, House, Temp, Humd, Moist)
            con.execute(query, params)
        
    except sql.Error as error:
        return


def main()->None:
    try:
        con = sql.connect("Main\\Monitor\\test.db")

        query = """CREATE TABLE IF NOT EXISTS example(
        DATETIME TEXT,
        HOUSE INTEGER,
        TEMP  REAL,
        HUMIDITY REAL,
        MOISTURE REAL
        );
        """
        con.execute(query)

        generate(con, 10000)
        con.commit()
        # query = """INSERT INTO example VALUES(?,?,?,?,?);"""

        # for _ in range(10000):
        #     dateRand = datetime(randint(2020, 2025), randint(1,12),randint(1,28), randint(0,23), randint(0,59))
        #     queryDT = dateRand.isoformat(sep=" ", timespec="minutes")
        #     House = randint(1,5)
        #     Temp  = round(random() % 20 + 20, 2)
        #     Humd  = round(random() % 100, 2)
        #     Moist = round(random() % 100, 2)

        #     params = (queryDT, House, Temp, Humd, Moist)
        #     con.execute(query, params)
        
        # con.commit()

    except sql.Error as error:
        print("Error occured - ", error)

    finally:
        if con:
            con.close()


if __name__ == "__main__":
    main()
            