#include <stdio.h>
#include <string.h>

int main() {
    char creditCardNumber[17];
    printf("Enter a 16-digit credit card number: ");
    scanf("%16s", creditCardNumber);

    // Check if the input length is valid
    if (strlen(creditCardNumber) != 16) {
        printf("Invalid input length. Please enter a 16-digit number.\n");
        return 1;
    }

    int sum = 0;
    printf("Initial sum: %d\n", sum);
    for (int i = 14; i >= 0; i -= 2) {
        int digit = (creditCardNumber[i] - '0') * 2;
        if (digit > 9) {
            digit = digit / 10 + digit % 10;
        }
        sum += digit;
    }
    printf("Sum after first loop: %d\n", sum);
    
    for (int i = 15; i >= 0; i -= 2) {
        int digit = creditCardNumber[i] - '0';
        sum += digit;
    }
    printf("Final sum: %d\n", sum);

    if (sum % 10 == 0) {
        printf("Valid card number\n");
    } else {
        printf("Invalid card number\n");
    }

    return 0;
}
