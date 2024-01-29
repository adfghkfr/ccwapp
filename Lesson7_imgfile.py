import sqlite3
from sqlite3 import Error
import os
 
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 
def fetch_paperid(conn):
    cur = conn.cursor()
    sql = "select id from papers"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows
     
def update_papers(conn, params):
     
    sql = "UPDATE papers set imgfile = ? WHERE id = ?"
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
 
def main():
    database = r"/Users/guoyixuan/Documents/pythoncode/ccwdatabase/homework.sqlite" # 資料庫的位置
    file_src = r"/Users/guoyixuan/Documents/pythoncode/ccwdatabase/NIP2015_Images/"  # 圖片檔的位置
    picName = os.listdir(file_src) #把圖片的檔名列出來

    print(picName)
    # create a database connection
    conn = create_connection(database)
    # fetch paper id
    paperid = fetch_paperid(conn) #拿到403個id
    with conn: #把id拿過來
        for i in range(len(paperid)):
            update_papers(conn, (picName[i], paperid[i][0]))
 
    conn.close()
 
if __name__ == '__main__':
    main()
import os

# Get the full path of the image file
image_path = os.path.abspath("image.jpg")

# Print the full path
print(image_path)

