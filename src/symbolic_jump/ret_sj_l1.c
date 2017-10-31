/*
TOY:
*/
#include <string.h> 
#include "utils.h"
#include "a_tester.h"

#define push(v) asm volatile ("push %0"::"m"(v))
#define pop(v) asm volatile ("pop %0":: "m"(v))
#define ret() asm volatile ("ret :: "m")
#define jmp(addr) asm("jmp *%0"::"r"(addr):)

int flag = 0;

void trigger() {
     flag = 1;
}

int logic_bomb(char* symvar) {
    int flag = 0;
    char* buf[2];
    strcpy(buf, symvar);
    if(flag == 1){
        return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
