import requests
from bs4 import BeautifulSoup
import pymysql
import time
import re
from collections import Counter


# -------- 配置数据库 --------
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Yu844958388',   # TODO: 换成你的 MySQL 密码
    charset='utf8mb4'
)
cursor = conn.cursor()

# 创建数据库和表
cursor.execute("CREATE DATABASE IF NOT EXISTS douban_movies DEFAULT CHARSET utf8mb4;")
cursor.execute("USE douban_movies;")
cursor.execute("""
CREATE TABLE IF NOT EXISTS top_movies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    rating FLOAT,
    director VARCHAR(255),
    actor VARCHAR(255),
    year INT,
    country VARCHAR(255),
    genre VARCHAR(255)
);
""")


# -------- 豆瓣爬虫函数 --------
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def fetch_movies(start):
    url = f"https://movie.douban.com/top250?start={start}&filter="
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('.item')

    movie_data = []
    for item in items:
        try:
            title = item.select_one('.title').text.strip()
            rating = float(item.select_one('.rating_num').text.strip())
            info_text = item.select('.bd p')[0].text.strip().split('\n')
            line1 = info_text[0].strip()
            line2 = info_text[1].strip() if len(info_text) > 1 else ""

            # line1: 导演 / 主演
            match_director = re.search(r'导演:([^/]+)', line1)
            match_actor = re.search(r'主演:([^/]+)', line1)
            director = match_director.group(1).strip() if match_director else ''
            actor = match_actor.group(1).strip() if match_actor else ''

            # line2: 年份 / 国家 / 类型
            parts = line2.split('/')
            year_raw = parts[0].strip() if len(parts) > 0 else ''
            match_year = re.search(r'\d{4}', year_raw)
            year = int(match_year.group()) if match_year else 0

            country = parts[1].strip() if len(parts) > 1 else ""
            genre = parts[2].strip() if len(parts) > 2 else ""

            movie_data.append((title, rating, director, actor, year, country, genre))
        except Exception as e:
            print("解析失败：", e)
            continue

    return movie_data


# -------- 插入数据库 --------
def insert_movies(movies):
    for movie in movies:
        try:
            cursor.execute("""
                INSERT INTO top_movies (title, rating, director, actor, year, country, genre)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, movie)
        except Exception as e:
            print("插入失败：", e)
    conn.commit()


# -------- 统计展示 --------
def show_stats():
    print("\n🎬 统计结果展示：")

    # 1. 出演次数最多的演员
    cursor.execute("""
        SELECT actor, COUNT(*) AS times FROM top_movies
        WHERE actor != ''
        GROUP BY actor ORDER BY times DESC LIMIT 1;
    """)
    actor, times = cursor.fetchone()
    print(f"\n▶ 出演次数最多的演员：{actor}（{times} 次）")

    # 2. 制片最多的国家
    cursor.execute("""
        SELECT country, COUNT(*) AS count FROM top_movies
        WHERE country != ''
        GROUP BY country ORDER BY count DESC LIMIT 1;
    """)
    country, count = cursor.fetchone()
    print(f"\n▶ 制片最多的国家：{country}（{count} 部）")

    # 3. 出现次数最多的导演
    cursor.execute("""
        SELECT director, COUNT(*) AS times FROM top_movies
        WHERE director != ''
        GROUP BY director ORDER BY times DESC LIMIT 1;
    """)
    director, times = cursor.fetchone()
    print(f"\n▶ 出现次数最多的导演：{director}（{times} 次）")

    # 4. 各类型电影数量（拆分统计）
    print("\n▶ 各类型电影数量：")
    cursor.execute("SELECT genre FROM top_movies WHERE genre != '';")
    genre_counter = Counter()
    for (genre_str,) in cursor.fetchall():
        genres = re.split(r'[ /]', genre_str.strip())  # 按空格或 / 拆分
        genre_counter.update([g for g in genres if g])

    for genre, count in genre_counter.most_common():
        print(f"{genre}: {count} 部")


# -------- 主执行流程 --------
def main():
    for start in range(0, 200, 25):  # Top200，每页25条
        print(f"正在爬取第 {start + 1} ~ {start + 25} 条电影...")
        movies = fetch_movies(start)
        insert_movies(movies)
        time.sleep(2)

    print("\n✅ 爬取完毕，共插入 200 部电影。")
    show_stats()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
