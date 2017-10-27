#include "a_tester.h"

int logic_bomb(int a) {
    if (a + 2147483640 < 0 && a > 0)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
