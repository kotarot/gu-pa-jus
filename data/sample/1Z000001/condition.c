#include <stdio.h>

int main(void) {
    int n;
    printf("Input a number: ");
    scanf("%d", &n);

    if (n >= 0) {
        printf("pos\n");
    } else {
        printf("neg\n");
    }

    return 0;
}
