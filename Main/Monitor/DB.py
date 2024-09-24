import sqlite3 as sql
from datetime import datetime
from random import random, randint

def main()->None:
    try:
        con = sql.connect("Main\\Monitor\\test.db")
        cursor = con.cursor()

        query = """CREATE TABLE IF NOT EXISTS example(
        DATETIME TEXT,
        HOUSE INTEGER,
        TEMP  REAL,
        HUMIDITY REAL,
        MOISTURE REAL
        );
        """
        con.execute(query)

        dateTime = datetime.now()
        dateRand = datetime(randint(2020, 2025), randint(1,12),randint(1,28), randint(0,23), randint(0,59))

        queryDT = dateTime.isoformat(sep=" ",timespec="minutes")
        otherTimes = ["2024-09-22 12:30",
                      "2024-10-22 12:20",
                      "2024-09-20 12:15",
                      "2024-09-25 12:10",
                      "2024-09-22 12:05"
                      ]
        
        otherTemps = [round(random()% 20 + 20, 2) for _ in range(5)]
        otherHums  = [round(random()% 100, 2)     for _ in range(5)]
        otherMoist = [round(random()% 100, 2)     for _ in range(5)]

        query = """INSERT INTO example VALUES(?,?,?,?,?);"""
        con.execute(query,(queryDT, 1, 30.0, 25.0, 10.0))

        for i in range(5):
            con.execute(query, (otherTimes[i], 1, otherTemps[i], otherHums[i], otherMoist[i]))

        con.commit()

        cursor.execute("SELECT * FROM example ORDER BY DATETIME;")
        for i in cursor:
            print("{} {} {} {} {}".format(i[0],i[1],i[2],i[3],i[4]))
        

    except sql.Error as error:
        print("Error occured - ", error)

    finally:
        if con:
            con.close()


if __name__ == "__main__":
    main()