#include <string.h> 
#include "utils.h"

#include "a_tester.h"

// {"s":{"length": 16}}
int logic_bomb(char* s) {
    int trigger = 0;
    int fd = open(s, O_RDONLY);
    if(fd != -1) {
    	trigger = 1;
        close(fd);
    }

    if(trigger) {
        return BOMB_ENDING;
    } else {
        return NORMAL_ENDING;
    }
}
