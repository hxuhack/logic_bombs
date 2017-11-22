/*
TOY:
*/
#include <string.h> 
#include <math.h>
#include "utils.h"
#include "a_tester.h"

// {"s":{"length": 4}}
int logic_bomb(char* s) {
    int symvar = s[0] - 48;
    if(pow(symvar, 2) == 49){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
