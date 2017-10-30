#include "a_tester.h"

//#define push(v) asm volatile ("push %0"::"m"(v))

int logic_bomb(int i) {
    int j;
    __asm__ __volatile__("push %0" :: "m"(i));
    __asm__ __volatile__("pop %0" :: "m"(j));
    printf("%d\n", j);
    if(j == 7){
        printf("Bobm \n");
        return 1;
        //return BOMB_ENDING;
    } else{
        printf("Normal \n");
	return 0;
        //return NORMAL_ENDING;
    }
}
