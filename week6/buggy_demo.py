
def calculate_average(scores):
    """计算分数平均值 - 这里有潜在Bug"""
    total = 0
    for score in scores:
        total += score
    # Bug: 如果scores是空列表会怎样？
    return total / len(scores)

def main():
    print("分数平均值计算器")
    
    # Bug: 如果用户输入非数字会怎样？
    n = int(input("要输入多少个分数？ "))
    
    scores = []
    for i in range(n):

        score = int(input(f"输入第{i+1}个分数: "))
        scores.append(score)
    
    print(f"收集到的分数: {scores}")
    
    # 计算平均值
    average = calculate_average(scores)
    print(f"平均分: {average}")

if __name__ == "__main__":
    main()
