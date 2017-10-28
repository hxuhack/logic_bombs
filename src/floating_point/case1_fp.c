#include<stdio.h>
#include "a_tester.h"

int logic_bomb(float symvar) {
    printf("symvar = %f\n", symvar);
    float x = symvar;
    printf("x = %f\n", x);
    if(1024+x == 1024 && x>0)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
