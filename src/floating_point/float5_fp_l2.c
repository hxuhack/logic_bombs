#include<stdio.h>
#include <stdlib.h>
#include "a_tester.h"

int logic_bomb(float symvar) {
    float x = symvar/10.0;
    x = x + 0.1;
    x = x * x;
    if (x > 0.1)
	x -= x;
    else
        printf("x = %f\n", x);
    if(x != 0.02){
        x = x + 7.98;
        printf("x = %f\n", x);
        if(x == 8)
            return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
