#include <string.h> 
#include "utils.h"
#include "a_tester.h"

int trigger(){
    return BOMB_ENDING;
}

// {"symvar":{"length": 128}}
int logic_bomb(char* symvar) {
    char buf[8];
    strcpy(buf, symvar);
    if(buf < 0)
        return trigger();
    return NORMAL_ENDING;
}
