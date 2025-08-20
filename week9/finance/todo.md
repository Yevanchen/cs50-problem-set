- 实现登录功能
- 实现注册功能（数据库变更）

- 我现在需要一个 buy 的 function实现
 - 因为其买入和卖出 认为市场行为只发生在用户-市场
 - 用户的购买不会对市场本身产生影响
 - 用户行为：用户 lookup 某股票 然后可以以当前价格采购 会发生一条购买记录
 - user action（buy） symbol 股数 成交总价  

- 我需要一个资产表，显示用户当前持有的股票：symbol、股数、估值（当前价格 * 股数）

-- 重新创建表（使用英文字段名）
CREATE TABLE actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    total_amount NUMERIC NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);