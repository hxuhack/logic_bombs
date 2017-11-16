#include <stdio.h>
#include "utils.h"

#define jmp(addr) asm("jmp *%0"::"r"(addr):)

#include "a_tester.h"

int logic_bomb(int symvar) {
    int array[] = {0,7,13,14,15,16,21,22,23,24,31,37};
    long long addr = &&flag_0 + array[symvar%12];
    jmp(addr);
  flag_0:
    if (symvar > 0){
        symvar++;
        if(symvar == 0)
            return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
