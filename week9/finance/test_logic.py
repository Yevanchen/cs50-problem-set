#!/usr/bin/env python3

import sqlite3

def test_database_logic():
    """测试数据库逻辑"""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    print("=== 当前数据库状态 ===")
    
    # 检查用户表
    print("\n1. 用户表:")
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(f"   ID: {user[0]}, 用户名: {user[1]}, 现金: ${user[3]}")
    
    # 检查交易记录表
    print("\n2. 交易记录表:")
    cursor.execute("SELECT * FROM actions ORDER BY timestamp")
    actions = cursor.fetchall()
    for action in actions:
        print(f"   ID: {action[0]}, 用户ID: {action[1]}, 操作: {action[2]}, 股票: {action[3]}, 股数: {action[4]}, 价格: ${action[5]}, 总金额: ${action[6]}, 时间: {action[7]}")
    
    # 检查资产表
    print("\n3. 资产表:")
    cursor.execute("SELECT * FROM assets")
    assets = cursor.fetchall()
    for asset in assets:
        print(f"   ID: {asset[0]}, 用户ID: {asset[1]}, 股票: {asset[2]}, 股数: {asset[3]}")
    
    # 验证逻辑一致性
    print("\n=== 逻辑验证 ===")
    
    # 计算用户1的AAPL总股数
    cursor.execute("SELECT SUM(shares) FROM actions WHERE user_id = 1 AND symbol = 'AAPL' AND action = 'buy'")
    total_bought = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(shares) FROM actions WHERE user_id = 1 AND symbol = 'AAPL' AND action = 'sell'")
    total_sold = cursor.fetchone()[0] or 0
    
    net_shares = total_bought - total_sold
    
    print(f"4. AAPL股票逻辑验证:")
    print(f"   总买入: {total_bought} 股")
    print(f"   总卖出: {total_sold} 股")
    print(f"   净持有: {net_shares} 股")
    
    # 检查资产表中的实际持有
    cursor.execute("SELECT shares FROM assets WHERE user_id = 1 AND symbol = 'AAPL'")
    asset_result = cursor.fetchone()
    if asset_result:
        actual_shares = asset_result[0]
        print(f"   资产表显示: {actual_shares} 股")
        if actual_shares == net_shares:
            print("   ✅ 逻辑一致！")
        else:
            print(f"   ❌ 逻辑不一致！应该显示 {net_shares} 股")
    else:
        print("   资产表中没有AAPL记录")
    
    conn.close()

if __name__ == "__main__":
    test_database_logic()
