import sqlite3

# Connect to the database / Conectar a la base de datos
db = sqlite3.connect('ssh_changes.db')
cursor = db.cursor()

query = "SELECT * FROM changes"

cursor.execute(query)

results = cursor.fetchall()

for row in results:
    print(f"ID: {row[0]}")
    print(f"Event Type: {row[1]}")
    print(f"File Name: {row[2]}")
    print(f"Timestamp: {row[3]}")
    print("-" * 20)

db.close()
