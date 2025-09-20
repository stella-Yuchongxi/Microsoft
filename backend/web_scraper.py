import requests
from bs4 import BeautifulSoup
import pymysql

# 配置数据库信息
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Yu844958388",
    "database": "hot_search",
    "charset": "utf8mb4"
}

# 创建数据库连接
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

# 创建表（如果不存在）
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS baidu_hot_search (
            id INT AUTO_INCREMENT PRIMARY KEY,
            `rank` INT,
            title VARCHAR(255),
            url TEXT
        );
    """)
    conn.commit()
    conn.close()

# 爬取百度热搜榜Top5
def fetch_baidu_hot_search_top5():
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    top_list = []
    items = soup.select(".category-wrap_iQLoo.horizontal_1eKyQ")[:5]  # 前5条
    for idx, item in enumerate(items, 1):
        title = item.select_one(".c-single-text-ellipsis").get_text(strip=True)
        link = item.select_one("a")["href"]
        top_list.append((idx, title, link))

    return top_list

# 插入数据到数据库
def save_to_db(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE baidu_hot_search")  # 可选：清空表
    for rank, title, url in data:
        cursor.execute("INSERT INTO baidu_hot_search (`rank`, title, url) VALUES (%s, %s, %s)", (rank, title, url))
    conn.commit()
    conn.close()

# 主函数执行流程
if __name__ == "__main__":
    create_table()
    hot_search_data = fetch_baidu_hot_search_top5()
    save_to_db(hot_search_data)
    print("已成功写入Top5热搜到数据库！")
