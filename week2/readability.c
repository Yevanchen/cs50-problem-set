#include <stdio.h>

int main(void) {
    char name[50];
    printf("请输入你的名字: ");
    scanf("%s", name);
    printf("你好, %s!\n", name);
    return 0;
}
