#include <stdio.h>
#include <string.h>

// Function prototype
void reverseString(const char *str);

int main(void)
{
    int height;

    do {
        printf("Enter the height of the pyramid (1-8): ");
        scanf("%d", &height);
        
        if (height < 1 || height > 8) {
            printf("Invalid input. Please enter a number between 1 and 8.\n");
        }
    } while (height < 1 || height > 8);
    //当输入的height在1到8之间时，退出循环
    for (int i = 1; i <= height; i++) {
        // Print spaces
        for (int j = height - i; j > 0; j--) {
            printf(" ");
        }
        // Print hashes
        for (int k = 0; k < i; k++) {
            printf("#");
        }
        // Create a string to store the hashes
        char hashes[9] = {0}; // Max height is 8, plus 1 for null terminator
        for (int k = 0; k < i; k++) {
            hashes[k] = '#';
        }
        // Reverse the hashes string and print it
        printf("  ");
        reverseString(hashes);
        printf("\n"); // Print a newline after the pyramid
    }

    return 0;
}

void reverseString(const char *str) {
    int len = strlen(str);
    for (int i = len - 1; i >= 0; i--) {
        putchar(str[i]);
    }
}





