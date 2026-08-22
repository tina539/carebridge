import sqlite3
import os
import psycopg


# ========================================
# 1. 連接 SQLite
# ========================================

sqlite_conn = sqlite3.connect("carebridge.db")
sqlite_cursor = sqlite_conn.cursor()

print("SQLite 連線成功")


# ========================================
# 2. 取得 PostgreSQL DATABASE_URL
# ========================================



DATABASE_URL = "postgresql://postgres:1234@localhost:5432/carebridge"


# ========================================
# 3. 連接 PostgreSQL
# ========================================

pg_conn = psycopg.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

print("PostgreSQL 連線成功")


# ========================================
# 4. 建立 doctors
# ========================================

# 先清空舊結構重新建立
pg_cursor.execute("DROP TABLE IF EXISTS visits CASCADE;")
pg_cursor.execute("DROP TABLE IF EXISTS patients CASCADE;")
pg_cursor.execute("DROP TABLE IF EXISTS doctors CASCADE;")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    facility_id INTEGER
)
""")


# ========================================
# 5. 建立 patients
# ========================================

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date TEXT,
    gender TEXT,
    phone TEXT,
    disease TEXT,
    allergy TEXT,
    medication TEXT,
    id_number TEXT,
    family_history TEXT
)
""")


# ========================================
# 6. 建立 visits
# ========================================

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS visits (
    visit_id INTEGER PRIMARY KEY,
    patient_id TEXT NOT NULL,
    visit_date TEXT NOT NULL,
    status TEXT DEFAULT '已預約',
    chief_complaint TEXT,
    appointment_number INTEGER,
    appointment_time TEXT,
    checked_in_at TEXT,
    started_at TEXT,
    completed_at TEXT,
    diagnosis TEXT,
    prescription TEXT,
    ai_summary TEXT,
    facility_id TEXT
)
""")


print("PostgreSQL 資料表建立完成")

# ==========================================
# 建立 3 位預設醫生帳號
# ==========================================
print("正在建立預設醫生帳號...")

doctors_data = [
    (1, '慧慧', 'huihui', '1234', 1),
    (2, '賴賴', 'line', '4321', 3),
    (3, '甘甘', 'stella', '1002', 2)
]

for d in doctors_data:
    pg_cursor.execute("""
        INSERT INTO doctors (doctor_id, name, username, password, facility_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (doctor_id) DO UPDATE 
        SET name=EXCLUDED.name, username=EXCLUDED.username, password=EXCLUDED.password, facility_id=EXCLUDED.facility_id;
    """, d)


# ========================================
# 10. 提交
# ========================================

pg_conn.commit()

print()
print("========================================")
print("SQLite → PostgreSQL 搬移完成！")
print("========================================")


# ========================================
# 11. 驗證 PostgreSQL 筆數
# ========================================

for table in ["doctors", "patients", "visits"]:

    pg_cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = pg_cursor.fetchone()[0]

    print(f"{table}: {count} 筆")


# ========================================
# 12. 關閉
# ========================================

sqlite_conn.close()
pg_conn.close()

print()
print("連線已關閉")