#include<stdio.h>
#include <stdlib.h>
#include "a_tester.h"

int logic_bomb(float symvar) {
    float x = symvar/-10000.0;
    if(1024+x == 1024 && x>0)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
