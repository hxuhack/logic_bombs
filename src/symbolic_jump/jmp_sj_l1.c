#include <stdio.h>
#include "utils.h"

#define jmp(addr) asm("jmp *%0"::"r"(addr):)

#include "a_tester.h"

int logic_bomb(int symvar) {
    int x = symvar + 30;
    long long addr = &&flag_0 + x;
    if(x > 30 && x < 40){
        if (x % 6 == 1)
            jmp(addr);
    }
  flag_0:
    if (x > 0){
        x++;
        if(x == 0)
            return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
