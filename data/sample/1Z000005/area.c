#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int a, b;
    printf("Input a: ");
    scanf("%d", &a);
    printf("Input b: ");
    scanf("%d", &b);

    int s = a * b / 2;
    printf("The area is %d\n", s);
    system("hostname");

    return 0;
}
