"""批量将数据库中的图片数据同步到 Chroma 向量库"""

import json
import requests
import pymysql

# ===== 配置 =====
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "1234"
DB_NAME = "dam_picture"
EMBEDDING_API = "http://localhost:8000/embedding/add"


def get_connection():
    return pymysql.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME,
        charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
    )


def fetch_pictures(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, tags, category, introduction FROM picture WHERE isDelete = 0 AND spaceId IS NULL AND reviewStatus = 1")
        return cur.fetchall()


def add_embedding(picture):
    tags = picture.get("tags") or ""
    # tags 存的是 JSON 数组字符串，转成逗号分隔
    if tags.startswith("["):
        try:
            tags = ", ".join(json.loads(tags))
        except json.JSONDecodeError:
            pass

    payload = {
        "pictureId": picture["id"],
        "title": picture.get("name") or "",
        "tags": tags,
        "category": picture.get("category") or "",
        "description": picture.get("introduction") or "",
    }
    resp = requests.post(EMBEDDING_API, json=payload, timeout=60)
    return resp.status_code == 200


def main():
    conn = get_connection()
    pictures = fetch_pictures(conn)
    conn.close()

    total = len(pictures)
    print(f"共 {total} 张图片，开始同步向量...")

    success, fail = 0, 0
    for i, pic in enumerate(pictures, 1):
        try:
            if add_embedding(pic):
                success += 1
                print(f"[{i}/{total}] OK - {pic.get('name', pic['id'])}")
            else:
                fail += 1
                print(f"[{i}/{total}] FAIL - {pic.get('name', pic['id'])}")
        except Exception as e:
            fail += 1
            print(f"[{i}/{total}] ERROR - {pic.get('name', pic['id'])}: {e}")

    print(f"\n完成！成功 {success}，失败 {fail}")


if __name__ == "__main__":
    main()
