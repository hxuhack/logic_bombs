/*
TOY:
*/
#include <string.h> 
#include "utils.h"

#define push(v) asm volatile ("push %0"::"m"(v))
#define pop(v) asm volatile ("pop %0" :: "m"(v))

int main(int argc, char** argv){

    int j,i=atoi(argv[1]); 
    push(i); 
    //push(1); 
    pop (j);
    if(j == 7){
        Bomb();
    } else{
        Foobar();
    }
}
