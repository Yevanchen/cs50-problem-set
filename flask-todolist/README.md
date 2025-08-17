# Flask TodoList - Modern Web Application

一个基于 Flask 的现代化待办事项管理应用，采用前后端分离架构。

## 🚀 项目特色

### 核心功能
- ✅ **用户认证系统**：安全的注册、登录、会话管理
- ✅ **待办事项管理**：添加、编辑、完成、持久化存储
- ✅ **数据隔离**：每个用户拥有独立的待办清单
- ✅ **现代化架构**：RESTful API + 前后端分离

### 技术亮点
- 🏗️ **RESTful API 设计**：标准的 HTTP 方法和响应格式
- 🔒 **安全认证**：密码验证、会话管理、用户数据隔离  
- 📱 **响应式设计**：现代化 UI，支持多设备访问
- 🔄 **实时数据同步**：前端通过 API 与数据库实时交互

## 🛠️ 技术栈

**后端**
- Flask - Python Web 框架
- SQLite - 轻量级数据库
- Flask-Session - 会话管理

**前端**
- HTML5/CSS3 - 现代化界面
- JavaScript (ES6+) - 异步编程、API 调用
- Fetch API - 前后端数据交换

**架构模式**
- MVC 架构模式
- RESTful API 设计
- 前后端分离

## 📁 项目结构

```
flask-todolist/
├── app.py                 # Flask 主应用
├── schema.sql            # 数据库结构
├── todolist.db          # SQLite 数据库
├── requirements.txt      # Python 依赖
├── templates/           # HTML 模板
│   ├── layout.html      # 基础布局
│   ├── index.html       # 主页面
│   ├── login.html       # 登录页面
│   └── register.html    # 注册页面
└── static/             # 静态资源
    ├── css/
    │   └── style.css   # 样式文件
    └── js/
        └── script.js   # 前端逻辑
```

## 🗄️ 数据库设计

### users 表
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
```

### todos 表
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_content TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 🔌 API 接口

### 用户认证
- `POST /login` - 用户登录
- `POST /register` - 用户注册
- `GET /logout` - 用户登出

### 待办事项
- `GET /api/todos` - 获取用户的所有待办事项
- `POST /api/todos` - 添加新的待办事项
- `PUT /api/todos/<id>` - 更新待办事项（状态或内容）

### API 响应格式
```json
{
  "pending": [
    {
      "id": 1,
      "user_id": 1,
      "task_content": "学习 Flask",
      "status": "pending"
    }
  ],
  "completed": [
    {
      "id": 2,
      "user_id": 1,
      "task_content": "完成项目",
      "status": "completed"
    }
  ]
}
```

## 🚀 快速开始

### 环境要求
- Python 3.7+
- pip

### 安装和运行

1. **克隆或下载项目**
   ```bash
   cd flask-todolist
   ```

2. **安装依赖**
   ```bash
   pip install flask flask-session
   ```

3. **初始化数据库**
   ```bash
   sqlite3 todolist.db < schema.sql
   ```

4. **运行应用**
   ```bash
   python app.py
   ```

5. **访问应用**
   
   打开浏览器访问：`http://127.0.0.1:5000`

## 🎯 使用指南

### 首次使用
1. **注册账户**：点击 "Register" 创建新账户
2. **登录系统**：使用用户名和密码登录
3. **管理待办事项**：
   - 点击 "Add" 添加新任务
   - 点击任务内容进行编辑
   - 勾选复选框标记完成

### 功能说明
- **添加任务**：点击 "Add" 按钮创建空白任务，然后点击编辑
- **编辑任务**：点击任务内容，修改后点击其他地方保存
- **完成任务**：点击复选框，任务会移动到"已完成"区域
- **数据持久化**：所有操作都会实时保存到数据库

## 🏗️ 架构设计

### 前后端分离
```
前端 JavaScript ←→ REST API ←→ Flask 后端 ←→ SQLite 数据库
```

### 关键特性
- **异步通信**：前端使用 `fetch()` 与后端 API 通信
- **状态管理**：前端维护数据缓存，后端提供数据源
- **安全设计**：用户认证、数据隔离、SQL 注入防护

### 代码示例

**前端 API 调用**
```javascript
async function addTodo() {
    const response = await fetch('/api/todos', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({task_content: ''})
    });
    await loadTodos();
}
```

**后端 API 接口**
```python
@app.route("/api/todos", methods=["POST"])
def add_todo():
    task_content = request.get_json().get("task_content", "")
    conn.execute(
        "INSERT INTO todos (user_id, task_content, status) VALUES (?, ?, 'pending')",
        (session["user_id"], task_content)
    )
```

## 🔒 安全特性

- **密码验证**：完整的用户名+密码认证
- **会话管理**：安全的服务器端会话存储
- **数据隔离**：用户只能访问自己的数据
- **SQL 注入防护**：使用参数化查询
- **输入验证**：前后端双重验证

## 🚀 可扩展功能

### 已实现
- [x] 用户注册和登录
- [x] 添加、编辑、完成待办事项
- [x] 数据持久化
- [x] 用户数据隔离

### 可以增强
- [ ] 删除待办事项
- [ ] 任务优先级
- [ ] 截止日期
- [ ] 任务分类/标签
- [ ] 搜索和过滤
- [ ] 导出数据
- [ ] 移动端适配

## 📚 学习价值

这个项目展示了现代 Web 开发的核心概念：

1. **全栈开发**：前端+后端+数据库的完整解决方案
2. **RESTful 设计**：标准的 API 设计模式
3. **安全开发**：用户认证和数据保护
4. **现代前端**：异步编程和 API 集成
5. **数据库设计**：关系型数据库和 SQL 操作

## 🤝 贡献

这是一个学习项目，欢迎提出改进建议！

## 📝 许可证

MIT License

---

**开发者**: CS50 学习项目  
**完成时间**: 2024年  
**技术栈**: Flask + SQLite + JavaScript  
**架构**: 前后端分离 + RESTful API
