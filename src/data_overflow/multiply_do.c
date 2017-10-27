#include "a_tester.h"

int logic_bomb(int a) {
    if (3 * a < 0 && a > 0)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
