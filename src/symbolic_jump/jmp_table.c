#include <stdio.h>
#include "utils.h"

#define jmp(addr) asm("jmp *%0"::"r"(addr):)

#include "a_tester.h"

int sym_checker(int i) {
    int addrs[] = {0,&&flag_1-&&flag_0,&&flag_2-&&flag_0,&&flag_3-&&flag_0,&&flag_4-&&flag_0,&&flag_5-&&flag_0};
    //printf("%x,%x,%x,%x,%x,%x, %d\n", &&flag_0, &&flag_1, &&flag_2, &&flag_3, &&flag_4, &&flag_5, addr);
    jmp(&&flag_0 + addrs[atoi(i+1]);
    flag_0:
        return BOMB_ENDING;
    flag_1:
        return NORMAL_ENDING;
    flag_2:
        Foobar();
    flag_3:
        Foobar();
    flag_4:
        Foobar();
    flag_5:
    	return 0;
}
