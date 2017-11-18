#include "a_tester.h"

int logic_bomb(int symvar) {
    if (symvar + 2147483640 < 0 && symvar > 0)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
