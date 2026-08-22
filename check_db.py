from app import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

print("\n=== visits 資料表的真實欄位 ===")
cursor.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'visits';
""")
for col in cursor.fetchall():
    print(col)

print("\n=== patients 資料表的真實欄位 ===")
cursor.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'patients';
""")
for col in cursor.fetchall():
    print(col)
print("===============================\n")

conn.close()