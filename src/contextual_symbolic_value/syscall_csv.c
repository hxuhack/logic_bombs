/*
TOY:
*/
#include <string.h>
#include "utils.h"

#include "a_tester.h"

// {"s":{"length": 16}}
int logic_bomb(char* s) {
    int trigger = 0;
    trigger = system(s);
    if(trigger == 0) {
        return BOMB_ENDING;
    } else {
        return NORMAL_ENDING;
    }
}
