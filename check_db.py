from app import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("SELECT patient_id, name, id_number, phone, birth_date FROM patients ORDER BY patient_id DESC LIMIT 5;")
rows = cursor.fetchall()

print("\n--- 最近註冊的病患資料 ---")
for r in rows:
    print(r)
print("--------------------------\n")

conn.close()