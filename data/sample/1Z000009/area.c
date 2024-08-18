#include <stdio.h>

int main(void) {
    int a, b;
    printf("Input a: ");
    scanf("%d", &a);
    printf("Input b: ");
    scanf("%d", &b);

    int s = a * b / 2;
    printf("The area is %d\n", s);
    printf("1234567890\n");  // Disallowed number

    return 0;
}
