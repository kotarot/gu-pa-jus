#include <stdio.h>

int main(void) {
    int a, b, s;

    printf("Input a: ");
    scanf("%d", &a);
    printf("Input b: ");
    scanf("%d", &b);

    s = a * b / 2;

    printf("The area is %d\n", s);

    return 0;
}
