from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 根路径路由
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 搜索接口
@app.route('/search')
def search():
    keyword1 = request.args.get('keyword1', '').strip()
    keyword2 = request.args.get('keyword2', '').strip()
    exclude = request.args.get('exclude', '').strip()

    # 参数校验
    if not keyword1 and not keyword2:
        return jsonify({"error": "至少需要输入一个关键词"}), 400

    # 构建SQL查询
    query = "SELECT `课程名称`, `链接` FROM data_table WHERE "
    params = []
    
    if keyword1:
        query += "`课程名称` LIKE ? "
        params.append(f'%{keyword1}%')
    
    if keyword2:
        if keyword1:
            query += "AND "
        query += "`课程名称` LIKE ? "
        params.append(f'%{keyword2}%')
    
    if exclude:
        query += "AND `课程名称` NOT LIKE ? "
        params.append(f'%{exclude}%')
    
    query += "LIMIT 100"

    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        results = [
            {"课程名称": row[0], "链接": row[1]}
            for row in cursor.fetchall()
        ]
        return jsonify({"count": len(results), "data": results})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
