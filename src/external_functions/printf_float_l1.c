/*
TOY:
Solution: 7
*/
#include <string.h> 
#include "utils.h"
#include "a_tester.h"

int logic_bomb(float symvar) {
    printf("symvar = %f", symvar);
    if(symvar - 7 == 0){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
