/*
Solution: 1.0000001
*/
#include<stdio.h>
#include"utils.h"

#include "a_tester.h"

int sym_checker(float x) {
    if(1 + x == 2 && x != 1)
        return BOMB_ENDING;
    else
	    return NORMAL_ENDING;
}
