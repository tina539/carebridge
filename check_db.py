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

    # 1. 抓取實際欄位清單
    cur.execute("SELECT * FROM visits LIMIT 0;")
    actual_cols = [desc[0] for desc in cur.description]
    print(f"\n visits 實際欄位: {actual_cols}")

    # 2. 測試執行報錯的那句 SQL
    try:
        cur.execute("SELECT visit_id FROM visits LIMIT 1;")
        print(" `SELECT visit_id` 執行成功！")
    except Exception as e:
        conn.rollback()
        print(f"❌ 執行失敗: {e}")
        
        # 如果欄位是 id，更名為 visit_id
        if "id" in actual_cols and "visit_id" not in actual_cols:
            print("正在自動將 'id' 更名為 'visit_id'...")
            cur.execute("ALTER TABLE visits RENAME COLUMN id TO visit_id;")
            conn.commit()
            print("更名完成！請再試一次。")

    cur.close()
    conn.close()