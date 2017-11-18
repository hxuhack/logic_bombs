/*
TOY:
Solution: 7
*/
#include <string.h> 
#include "utils.h"
#include "a_tester.h"

int logic_bomb(int symvar) {
    int x = symvar + 190;
    printf("x = %d\n", x);
    if(x == 197){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
