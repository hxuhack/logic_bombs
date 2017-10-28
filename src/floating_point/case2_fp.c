/*
Solution: 1.0000001
*/
#include<stdio.h>

#include "a_tester.h"

int logic_bomb(float symvar) {
    printf("symvar = %f\n", symvar);
    float x = symvar;
    if(1 + x == 2 && x != 1)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
