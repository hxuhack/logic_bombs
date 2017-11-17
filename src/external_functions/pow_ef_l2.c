/*
TOY:
*/
#include <string.h> 
#include <math.h>
#include "utils.h"
#include "a_tester.h"

int logic_bomb(int i) {
    if(pow(i, 2) == 49){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
