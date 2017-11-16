#include <stdio.h>
#include "utils.h"

#define jmp(addr) asm("jmp *%0"::"r"(addr):)

#include "a_tester.h"

int logic_bomb(int symvar) {
    long long addr = &&flag_0 + symvar;
    if(symvar > 30 && symvar < 40){
        if (symvar%6 == 1)
            jmp(addr);
    }
  flag_0:
    if (symvar > 0){
        symvar++;
        if(symvar == 0)
            return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
