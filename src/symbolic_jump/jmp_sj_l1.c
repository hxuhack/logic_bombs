#include <stdio.h>
#include "utils.h"

#define jmp(addr) asm("jmp *%0"::"r"(addr):)

#include "a_tester.h"

int logic_bomb(int symvar) {
    long long addr = &&flag_0 + symvar;
    printf("addr = %x, \n", addr);
    if(symvar < 20){
        if (symvar%10%6 == 0)
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
