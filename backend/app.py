from flask import Flask, jsonify
from flask_cors import CORS
import pymysql
import re
from collections import Counter

app = Flask(__name__)
CORS(app)

# 数据库连接
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Yu844958388',
        database='douban_movies',
        charset='utf8mb4'
    )

# API 1：类型分布
@app.route('/api/genre-count')
def genre_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT genre FROM top_movies WHERE genre != '';")
    rows = cursor.fetchall()
    conn.close()

    counter = Counter()
    for (genre_str,) in rows:
        genres = re.split(r'[ /]', genre_str.strip())
        counter.update([g for g in genres if g])

    return jsonify([{"name": g, "value": c} for g, c in counter.items()])


# API 2：年份分布
@app.route('/api/year-count')
def year_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT year, COUNT(*) FROM top_movies GROUP BY year ORDER BY year ASC")
    data = [{"year": row[0], "count": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
