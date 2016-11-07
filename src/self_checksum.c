#include <stdio.h>
#include "utils.h"

#define jmp(addr) asm("jmp *%0"::"r"(addr):)

int main(int argc, char** argv){
    int addr = argv[0][0] - 23;
    if (argc > 1)
	addr = addr - 10;
    //printf("%x,%x,%x, %d\n", &&flag_0, &&flag_1, &&flag_2, addr);

    flag_0:
    	jmp(&&flag_0 + addr);
    flag_1:
        Bomb();
    flag_2:
        Foobar();
    return 0;
}
