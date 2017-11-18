#include <stdio.h>
#include "a_tester.h"

// {"s":{"length": 4}}
int logic_bomb(char* s) {
    int symvar = s[0] - 48;
    int a[] = {1, 2, 3, 4, 5, 6};
    if (a[symvar]<0 || a[symvar] > 6){
        return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
