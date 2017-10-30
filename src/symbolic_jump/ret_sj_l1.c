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

int logic_bomb(int i) {
    int j;
    push(i); 
    pop(j);
    if(j == 7){
        return BOMB_ENDING;
    } else{
        return NORMAL_ENDING;
    }
}
