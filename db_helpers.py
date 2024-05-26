import sqlite3
from datetime import datetime, timezone
import os

features = ["peakFreq"]

def create_table():
    conn = sqlite3.connect('audio.db')
    cursor = conn.cursor()
    table ="""CREATE TABLE AUDIO(
                    ts VARCHAR(255),
                    src VARCHAR(255), 
            """
    for feat in features:
        table+= feat + " REAL,"
    table = table[:-1]
    table +="""
                    );
            """
    cursor.execute(table)
    print("DB created successfully!")
    return True

def insert_record(src,res):
    local_time = datetime.now(timezone.utc).astimezone()
    ts = local_time.isoformat()
    formatted_res = ""
    for i in res:
        formatted_res+="'%s',"%(i)
    formatted_res = formatted_res[:-1]
    conn = sqlite3.connect('audio.db')
    cursor = conn.cursor()
    query = '''INSERT INTO AUDIO VALUES ('%s', '%s', %s)'''%(ts,src,formatted_res)
    print(query)
    cursor.execute(query)
    conn.commit() 
    conn.close()

if __name__ == '__main__':
    if not os.path.exists('audio.db'):
        create_table()
    insert_record("blaa",[1])
    insert_record("blaa",[2])