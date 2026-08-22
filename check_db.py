import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    print("找不到 DATABASE_URL")
else:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # 檢查 visits 的主鍵欄位
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'visits';
    """)
    cols = [r[0] for r in cur.fetchall()]
    print(f"目前資料庫存在的欄位: {cols}")
    
    if 'id' in cols and 'visit_id' not in cols:
        print(">>> 發現欄位名稱為 'id'，正在自動更名為 'visit_id'...")
        cur.execute("ALTER TABLE visits RENAME COLUMN id TO visit_id;")
        conn.commit()
        print(">>> 修改完成！已成功將欄位改為 'visit_id'")
    elif 'visit_id' in cols:
        print(">>> 欄位名稱確認為 'visit_id'，結構正確！")
        
    cur.close()
    conn.close()