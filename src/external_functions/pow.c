/*
TOY:
*/
#include <string.h> 
#include <math.h>
#include "utils.h"
#include "a_tester.h"

int sym_checker(int i) {
    if(pow(i, 2) == -1){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
