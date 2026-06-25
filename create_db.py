import MySQLdb

try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="")
    cursor = db.cursor()
    cursor.execute("DROP DATABASE IF EXISTS hospital_db")
    cursor.execute("CREATE DATABASE hospital_db")
    print("Database hospital_db reset successfully.")
    db.close()
except Exception as e:
    print(f"Error creating database: {e}")
