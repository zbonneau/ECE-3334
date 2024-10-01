import sqlite3 as sql
import matplotlib.pyplot as plot
import pandas as pd
import DBFunc as db
import DBGenerator as generator

def getWindow(con:sql.Connection, dateStart: str, dateEnd: str)->pd.DataFrame:
    try:
        query = """SELECT * FROM example 
        WHERE DATETIME BETWEEN ? AND ? 
        ORDER BY DATETIME;"""
        df:pd.DataFrame = pd.read_sql_query(query, con, params=(dateStart, dateEnd))
        return df
    
    except sql.Error as error:
        return None
    
def drawGraph(df:pd.DataFrame, x: str, y:list[str])->None:
    plot.style.use("_mpl-gallery")

    x_axis = df[x]
    y_axis = df[y]

    fig, ax = plot.subplots()

    ax.plot(x_axis, y_axis)
    plot.show()

# def getData(con:sql.Connection, dateStart:str, dateEnd: str)->tuple[tuple[any]]:
#     try:
#         cursor:sql.Cursor = con.cursor()

#         query = """
#         SELECT 
#         """

def main():
    con = sql.connect("Main\\Monitor\\test.db")

    generator.generate(con, 10000)

    df = getWindow(con, "2024", "2024-12-31")
    df.describe()

    con.close()

    drawGraph(df, "DATETIME", ["TEMP", "HUMIDITY", "MOISTURE"])


if __name__ == "__main__":
    main()