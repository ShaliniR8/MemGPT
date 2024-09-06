import sqlite3
import uuid

def get_agent_id():
    conn = sqlite3.connect('C:/Users/Shalini Roy/.memgpt/sqlite.db')
    cursor = conn.cursor()

    query = "select id from agents"
    cursor.execute(query)
    agent_id = cursor.fetchall()[0][0]
    print(agent_id)
    return agent_id

def transfer_memory(old_id):
    new_id = uuid.uuid4()
    replace_ids(old_id, new_id)

def replace_ids(old_id, new_id):
    conn = sqlite3.connect('C:/Users/Shalini Roy/.memgpt/sqlite.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master 
    WHERE type='table' AND sql LIKE '%agent_id%';
    """)

    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        update_query = f"UPDATE {table_name} SET agent_id = '{new_id}';"
        cursor.execute(update_query)

    update_query = f"UPDATE agents SET id = '{new_id}';"
    cursor.execute(update_query)
    
    conn.commit()
    conn.close()



    conn = sqlite3.connect('C:/Users/Shalini Roy/.memgpt/chroma/chroma.sqlite3')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master 
    WHERE type='table' AND sql LIKE '%agent_id%';
    """)

    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        update_query = f"UPDATE {table_name} SET agent_id = '{new_id}';"
        cursor.execute(update_query)
    conn.commit()
    conn.close()