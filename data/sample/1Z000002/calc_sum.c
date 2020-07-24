#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp = fopen("numbers.txt", "r");
    if (fp == NULL) {
        printf("Open error\n");
        exit(1);
    }

    int sum = 0;
    int n;
    for (int i = 0; i < 3; i++) {
        fscanf(fp, "%d", &n);
        printf("%d\n", n);
        sum -= n;
    }
    printf("%d\n", sum);
    fclose(fp);

    return 0;
}
