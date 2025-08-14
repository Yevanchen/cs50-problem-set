# 简化的DAG调试示例
import pdb

class DAGNode:
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.has_breakpoint = False
        self.failed = False
        
    def set_breakpoint(self):
        self.has_breakpoint = True
        print(f"🔴 在节点 {self.name} 设置断点")
        return self
        
    def execute(self, data):
        print(f"\n🔄 执行节点: {self.name}")
        
        # 断点检查
        if self.has_breakpoint:
            print(f"⏸️  断点触发: {self.name}")
            pdb.set_trace()
            
        try:
            result = self.func(data)
            print(f"✅ {self.name} 成功: {result}")
            return result
        except Exception as e:
            self.failed = True
            print(f"❌ {self.name} 失败: {e}")
            # 关键：失败时也能调试
            print("🚨 异常调试模式")
            pdb.set_trace()  # 在异常处暂停
            raise

# 测试函数
def calculate_avg(scores):
    if len(scores) == 0:
        raise ValueError("空列表无法计算平均值")
    return sum(scores) / len(scores)

def find_max(scores):
    if not scores:
        raise ValueError("空列表无法找到最大值") 
    return max(scores)

# 主程序
print("=== DAG调试功能演示 ===")

# 创建节点并设置断点
node1 = DAGNode("avg_calculator", calculate_avg).set_breakpoint()
node2 = DAGNode("max_finder", find_max).set_breakpoint()

# 测试数据 - 空列表会触发错误
test_data = []

try:
    node1.execute(test_data)
except:
    print("节点1执行失败，但断点功能仍然可用")

try:
    node2.execute(test_data)
except:
    print("节点2执行失败，演示完成")
