#include <string.h> 
#include "utils.h"
#include "a_tester.h"


// {"symvar":{"length": 64}}
int logic_bomb(char* symvar) {
    int flag = 0;
    char buf[8];
    if(strlen(symvar) > 9)
        return NORMAL_ENDING;
    strcpy(buf, symvar);
    if(flag == 1){
        return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
