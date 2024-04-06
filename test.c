#include <stdio.h>
#include <stdlib.h>

int main() 
{
    // printf("Hello, World!\n");
    // float a = 3.14;
    // float* b = &a;

    float* a = (float*)malloc(sizeof(float));
    *a = 3.14;
    int b = a;
    printf("%f\n", *a);
    printf("%d\n", a);
    printf("%d\n", b);
    float *c;
    c = b;
    printf("%f\n", *c);
    free(a);
    return 0;
}