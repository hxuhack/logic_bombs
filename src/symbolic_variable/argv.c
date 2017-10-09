/*
--Triton: 
--Angr:
--BAP:
*/

#include "utils.h"

#include "a_tester.h"

int sym_checker(char** argv) {
    if(strlen(argv[1])==10){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
