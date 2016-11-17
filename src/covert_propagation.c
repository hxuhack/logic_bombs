/*
TOY:
*/
#include <string.h> 
#include "utils.h"

#define push(v) asm volatile ("push %0"::"m" (v))
#define pop(v) asm volatile ("pop %0"::"m" (v))

int main(int argc, char** argv){

    int i=atoi(argv[1]); 
    int tmp;
    push(i); 
    pop (tmp);
    if(tmp == 10){
        Bomb();
    } else{
        Foobar();
    }
}
