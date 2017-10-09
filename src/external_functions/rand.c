/*
TOY:
Solution: 7
*/
#include <string.h> 
#include "utils.h"
#include "a_tester.h"

int sym_checker(int i) {
    srand(i);
    int r = rand()%100;
    if(r == 77){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
