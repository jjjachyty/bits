import sqlite3




def insertData(titles,cnyprices,usdprices,types,times):
    conn = sqlite3.connect('/DATA/Work/DEV/python/workspace/Trust/db.sqlite3')
    c = conn.cursor()
    print("Opened database successfully")

    c.execute("INSERT INTO price (title,cnyprice,usdprice,type,time) VALUES (?,?,?,?,?)",[titles, cnyprices, usdprices,types,times]);
    conn.commit()
    conn.close()