#include <stdio.h>
#include <unistd.h>

int main(void) {
    int a, b;
    printf("Input a: ");
    scanf("%d", &a);
    printf("Input b: ");
    scanf("%d", &b);

    sleep(15);
    int s = a * b / 2;
    printf("The area is %d\n", s);

    return 0;
}
