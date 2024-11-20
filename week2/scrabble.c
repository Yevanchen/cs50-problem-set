#include <stdio.h>

int main(void)
{
    // Points assigned to each letter of the alphabet (A-Z)
    const int POINTS[26] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

    char word1[50], word2[50];
    printf("Player 1: ");
    scanf("%s", word1);
    printf("Player 2: ");
    scanf("%s", word2);

    int score1 = 0, score2 = 0;
    
    // Calculate score for player 1
    for (int i = 0; word1[i] != '\0'; i++) {
        char c = word1[i];
        // Convert to uppercase if lowercase
        if (c >= 'a' && c <= 'z') {
            c = c - 'a' + 'A';
        }
        // Calculate score if it's a letter
        if (c >= 'A' && c <= 'Z') {
            score1 += POINTS[c - 'A'];
        }
    }

    // Calculate score for player 2 
    for (int i = 0; word2[i] != '\0'; i++) {
        char c = word2[i];
        // Convert to uppercase if lowercase
        if (c >= 'a' && c <= 'z') {
            c = c - 'a' + 'A';
        }
        // Calculate score if it's a letter
        if (c >= 'A' && c <= 'Z') {
            score2 += POINTS[c - 'A'];
        }
    }

    // Compare scores and print winner
    if (score1 > score2) {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1) {
        printf("Player 2 wins!\n"); 
    }
    else {
        printf("Tie!\n");
    }
    return 0;
}
