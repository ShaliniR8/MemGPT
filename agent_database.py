import sqlite3

def get_agent_id():
    conn = sqlite3.connect('C:/Users/Shalini Roy/.memgpt/sqlite.db')
    cursor = conn.cursor()

    query = "select id from agents"
    cursor.execute(query)
    agent_id = cursor.fetchall()[0][0]
    print(agent_id)
    return agent_id

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
        update_query = f"UPDATE {table_name} SET agent_id = '001';"
        cursor.execute(update_query)
        print(f"Updated {table_name} with agent_id = '001'")

    conn.close()

    conn = sqlite3.connect('C:/Users/Shalini Roy/.memgpt/chroma/chroma.sqlite3')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master 
    WHERE type='table' AND sql LIKE '%agent_id%';
    """)

    results = cursor.fetchall()
    for row in results:
        print(f"Table: {row[0]}")

    conn.close()
