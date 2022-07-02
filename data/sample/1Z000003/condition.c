#include <stdio.h>

int main(void) {
    int n;
    printf("Input a number: ");
    scanf("%d", &n);

    if (n >= 0) {
        printf("正\n");
    } else {
        printf("負\n");
    }

    return 0;
}
