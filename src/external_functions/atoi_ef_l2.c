/*
TOY:
*/
#include <string.h> 
#include <math.h>
#include "utils.h"
#include "a_tester.h"

// {"s":{"length": 3}}
int logic_bomb(char* symvar) {
    int i = atoi(symvar);
    if(i==7){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
