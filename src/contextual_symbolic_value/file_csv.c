#include <string.h> 
#include "utils.h"

#include "a_tester.h"

// {"s":{"length": 16}}
int logic_bomb(char* s) {
    int trigger = 0;
    FILE *fp = fopen(s, "r");
    if(fp != NULL) {
	trigger = 1;
        fclose(fp);
    }

    if(trigger) {
        return BOMB_ENDING;
    } else {
        return NORMAL_ENDING;
    }
}
