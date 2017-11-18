/*
TOY:
Solution: 7
*/
#include <string.h> 
#include "utils.h"
#include "a_tester.h"

int logic_bomb(float symvar) {
    float x = symvar + 190;
    printf("x = %f\n", x);
    if(x - 197 == 0){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
