#include "a_tester.h"

int logic_bomb(int symvar) {
    if (254748364 * symvar < 0 && symvar > 0)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
