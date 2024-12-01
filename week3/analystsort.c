#include <stdio.h>
#include <time.h>

int main() {
    clock_t start, end;
    double cpu_time_used;

    // 记录开始时间
    start = clock();

    // 在这里放置需要计时的代码
    
    // 记录结束时间
    end = clock();
    
    // 计算运行时间（以秒为单位）
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    
    printf("程序运行时间: %f 秒\n", cpu_time_used);
    
    return 0;
}
