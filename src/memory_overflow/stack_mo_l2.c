#include <string.h> 
#include "utils.h"
#include "a_tester.h"

int logic_bomb(char* symvar) {
    char buf[8];
    strcpy(buf, symvar);
    if(buf[0] < 0)
        return BOMB_ENDING;
    return NORMAL_ENDING;
}
