/*
TOY:
Solution: 7
*/
#include <string.h> 
#include "utils.h"
#include "a_tester.h"

int logic_bomb(int symvar) {
    printf("symvar = %d", symvar);
    if(symvar == 7){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
