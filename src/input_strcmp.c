/*
TOY:
*/
#include <string.h> 
#include "utils.h"

int main(int argc, char** argv){
    char str[] = "bomb"; 
    if(strcmp(str, argv[1])==0){
        Bomb();
    }else{
        Foobar();
    }
}
