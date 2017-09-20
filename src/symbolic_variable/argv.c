/*
--Triton: 
--Angr:
--BAP:
*/

#include "utils.h"

int main(int argc, char** argv){
    if(strlen(argv[1])==10){
       Bomb();
    }else{
       Foobar();
    }
}
