/*
TOY:
*/
#include <string.h> 
#include <math.h>
#include "utils.h"
#include "a_tester.h"

int logic_bomb(int i) {
    double d = log(i); 
    if(1.94 < d && d < 1.95){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
