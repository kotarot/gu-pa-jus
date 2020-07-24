#include <stdio.h>
#include <math.h>

int main(void) {
    double r = 100;
    double s = pow(r, 2) * M_PI;
    s += 0.000001;
    printf("The area is %f\n", s);

    return 0;
}
