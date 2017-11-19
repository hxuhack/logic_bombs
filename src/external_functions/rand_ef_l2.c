/*
TOY:
Solution: 7
*/
#include <string.h> 
#include "utils.h"
#include "a_tester.h"

// {"s":{"length": 4}}
int logic_bomb(char* s) {
    int symvar = s[0];
    srand(symvar);
    int r = rand()%100;
    if(r == 77){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
