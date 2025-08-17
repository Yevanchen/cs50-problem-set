from flask_session import Session
from flask import Flask, render_template, request, session, redirect, jsonify, flash
import sqlite3

# 配置 Flask 应用
app = Flask(__name__)

app.config["SECRET_KEY"] = "1234567890"  # 生产环境要用随机密钥
# 配置 session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# 数据库文件路径
DATABASE = 'todolist.db'

# 数据库连接帮助函数
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    # 主页路由 - 需要检查登录状态
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and user["password"] == password:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")
    

@app.route("/register", methods=["GET", "POST"])  
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # 检查用户名是否已存在
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user:
            return render_template("register.html", error="Username already exists")
        # 注册用户
        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        flash("Registration successful! Please log in.", "success")
        return redirect("/login")




    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/api/todos", methods=["GET"])
def get_todos():
    """获取当前用户的所有待办事项"""
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401
    
    user_id = session["user_id"]
    conn = get_db_connection()
    
    # 获取待办事项，按状态分组
    pending_todos = conn.execute(
        "SELECT * FROM todos WHERE user_id = ? AND status = 'pending' ORDER BY id DESC",
        (user_id,)
    ).fetchall()
    
    completed_todos = conn.execute(
        "SELECT * FROM todos WHERE user_id = ? AND status = 'completed' ORDER BY id DESC", 
        (user_id,)
    ).fetchall()
    
    conn.close()
    
    return jsonify({
        "pending": [dict(todo) for todo in pending_todos],
        "completed": [dict(todo) for todo in completed_todos]
    })

@app.route("/api/todos", methods=["POST"])
def add_todo():
    """添加新的待办事项"""
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401
    
    task_content = request.get_json().get("task_content", "")
    
    user_id = session["user_id"]
    conn = get_db_connection()
    
    # 插入新的待办事项
    conn.execute(
        "INSERT INTO todos (user_id, task_content, status) VALUES (?, ?, 'pending')",
        (user_id, task_content)
    )
    conn.commit()
    
    # 获取新插入的记录
    new_todo = conn.execute(
        "SELECT * FROM todos WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user_id,)
    ).fetchone()
    
    conn.close()
    
    return jsonify({"todo": dict(new_todo)}), 201

    

@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """更新待办事项（状态或内容）"""
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401
    
    data = request.get_json()
    user_id = session["user_id"]
    
    conn = get_db_connection()
    
    # 🚀 只更新传递的字段
    update_fields = []
    params = []
    
    if "status" in data:
        update_fields.append("status = ?")
        params.append(data["status"])
    
    if "task_content" in data:
        update_fields.append("task_content = ?")
        params.append(data["task_content"])
    
    if update_fields:
        sql = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ? AND user_id = ?"
        params.extend([todo_id, user_id])
        
        conn.execute(sql, params)
        conn.commit()
    
    conn.close()
    return jsonify({"success": True})
    
    

if __name__ == "__main__":
    app.run(debug=True)