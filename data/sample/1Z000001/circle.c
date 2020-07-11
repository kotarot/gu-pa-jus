#include <stdio.h>
#include <math.h>

int main(void) {
    double r;
    printf("Input r: ");
    scanf("%lf", &r);

    double s = pow(r, 2) * M_PI;
    printf("The area is %f\n", s);

    return 0;
}
