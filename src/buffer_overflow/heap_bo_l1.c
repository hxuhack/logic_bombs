// {"s":{"length": 256}}
#include <string.h> 
#include "utils.h"
#include "a_tester.h"

int n = 5;
int logic_bomb(char* symvar) {
    char *p, *q;
    p = malloc(16);
    q = malloc(16);
    strcpy(p, symvar);
    free(q);
    if (n != 5){
        free(p);
        return BOMB_ENDING;
    }else {
        free(p);
        return NORMAL_ENDING;
    }
}
