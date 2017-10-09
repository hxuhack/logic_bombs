/*
TOY:
*/
#include <string.h> 
#include "utils.h"

#include "a_tester.h"

int sym_checker(char* str) {

    int trigger = 0; 
    trigger=system(str);

    printf ("%d\n", trigger);
    if(trigger == 0){
        return BOMB_ENDING;
    } else{
        return NORMAL_ENDING;
    }
}
