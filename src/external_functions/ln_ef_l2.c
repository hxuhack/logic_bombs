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
    double d = log(symvar); 
    if(1.94 < d && d < 1.95){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
