/*
TOY:
*/
#include <string.h>
#include "utils.h"

#include "a_tester.h"

// {"s":{"length": 16}}
int sym_checker_mannual(char* s) {
    int trigger = 0;
    trigger = system(s);

    printf ("%d\n", trigger);
    if(trigger == 0) {
        return BOMB_ENDING;
    } else {
        return NORMAL_ENDING;
    }
}
