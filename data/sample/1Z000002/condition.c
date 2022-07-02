#include <stdio.h>

int main(void) {
    int n;
    printf("Input a number: ");
    scanf("%d", &n);

    if (n >= 0) {
        printf("POS\n");
    } else {
        printf("NEG\n");
    }

    return 0;
}
