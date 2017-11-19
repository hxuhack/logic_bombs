#include "a_tester.h"

// {"s":{"length": 4}}
int logic_bomb(char* s) {
    int symvar = s[0] - 48;
    if (symvar + 2147483640 < 0 && symvar > 0)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
