#include <stdio.h>
#include <string.h>
void substitute(char *key, char *text);

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: ./substitution key\n"); 
        return 1;
    }

    char *key = argv[1];
    int key_length = strlen(key);

    if (key_length != 26) {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    int used[26] = {0}; // 用于追踪已使用的字母
    for (int i = 0; i < 26; i++) {
        // 转换为大写以简化检查
        char c = key[i];
        if (c >= 'a' && c <= 'z') {
            c = c - 'a' + 'A';
        }
        
        // 检查是否是字母
        if (c < 'A' || c > 'Z') {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }
        
        // 检查重复
        if (used[c - 'A']) {
            printf("Key must not contain repeated characters.\n");
            return 1;
        }
        used[c - 'A'] = 1;
    }
    char plaintext[1000];
    printf("plaintext: ");
    fgets(plaintext, sizeof(plaintext), stdin);
    plaintext[strcspn(plaintext, "\n")] = '\0';

    substitute(key, plaintext);
    printf("ciphertext: %s\n", plaintext);
    return 0;
}

void substitute(char *key, char *text) {
    // Check if all characters are alphabetic
    

    // Create mapping from key
    char mapping[26];
    for (int i = 0; i < 26; i++) {
        mapping[i] = key[i];
        if (mapping[i] >= 'a' && mapping[i] <= 'z') {
            mapping[i] = mapping[i] - 'a' + 'A';
        }
    }
    
    // Process each character in text
    for (int i = 0; text[i] != '\0'; i++) {
        if (text[i] >= 'A' && text[i] <= 'Z') {
            // Convert uppercase letters
            int index = text[i] - 'A';
            text[i] = mapping[index];
        }
        else if (text[i] >= 'a' && text[i] <= 'z') {
            // Convert lowercase letters
            int index = text[i] - 'a'; 
            text[i] = mapping[index] + ('a' - 'A');
        }
        else {
            // Non-alphabetic characters remain unchanged
            text[i] = text[i];
        }
    }
    
}


