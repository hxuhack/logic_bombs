/*
*solution: argv[1] = 0.00001
*/
#include<stdio.h>
#include "a_tester.h"

int sym_checker(float x) {
    if(1024+x==1024 && x>0)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
