import psycopg2

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "demodb"
DB_USER = "postgres"
DB_PASSWORD = "Sanya@121"  # ← Make sure you define this

try:
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = connection.cursor()  # ← add () to create the cursor
    print("PostgreSQL Connection Successful!")

    # Fetch all table names in 'public' schema
    cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public';
    """)

    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])

except Exception as e:
    print("Error:", e)

finally:
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()
