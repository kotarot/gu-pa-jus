#include <stdio.h>

int main(void) {
    int a, b;
    printf("Input a: ");
    scanf("%d", &a);
    printf("Input b: ");
    scanf("%d", &b);

    int s = a * b / 2;
    if (100 < s) {
        s = 100;
    }
    printf("The area is %d\n", s);

    return 0;
}
