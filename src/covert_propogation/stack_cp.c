#include "a_tester.h"

//#define push(v) asm volatile ("push %0"::"m"(v))

int logic_bomb(int i) {
    int j;
    __asm__ __volatile__("push %0" :: "m"(i));
    __asm__ __volatile__("pop %0" :: "m"(j));
    if(j == 7){
        return BOMB_ENDING;
    } else{
        return NORMAL_ENDING;
    }
}
