#include <string.h> 
#include "utils.h"
#include "a_tester.h"

int logic_bomb(char* symvar) {
    char* buf[8];
    int flag = 0;
    strcpy(buf, symvar);
    if(buf[0] < 0)
	flag ++;
    if(flag == 1){
        return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
