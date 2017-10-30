#include <stdio.h>
#include "utils.h"

#define jmp(addr) asm("jmp *%0"::"r"(addr):)

#include "a_tester.h"

int logic_bomb(int symvar) {
    int array[] = {0,4,6,10,14,16};
    long long addr = &&flag_0 + array[symvar%6];
    printf("addr = %x, \n", addr);
    jmp(addr);
  flag_0:
    if (symvar > 0){
        symvar++;
        if(symvar == 0)
            return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
