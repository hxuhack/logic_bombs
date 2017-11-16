#include<stdio.h>
#include <stdlib.h>
#include "a_tester.h"

int logic_bomb(int symvar) {
    float a = symvar/70.0;
    float b = 0.1;
    if(a != 0.1){
	if(a - b == 0)
            return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
