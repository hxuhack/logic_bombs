#include <stdio.h>
#include "a_tester.h"


int logic_bomb(int i) {
    int a[] = {1, 2, 3, 4, 5, 6};
    if (a[i]<0 || a[i] > 6){
        return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
