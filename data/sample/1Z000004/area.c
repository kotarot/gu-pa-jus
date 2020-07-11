#include <stdio.h>
#include <math.h>

int main(void) {
    int a, b;
    printf("Input a: ");
    scanf("%d", &a);
    printf("Input b: ");
    scanf("%d", &b);

    int s = (int)pow(a * b / 2, 1.0);
    printf("The area is %d\n", s);

    return 0;
}
