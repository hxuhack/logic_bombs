/*
TOY:
*/
#include <string.h> 
#include "utils.h"

int main(int argc, char** argv){
    int i = atoi(argv[1]);
    if(pow(i, 0.5) == 7){
        Bomb();
    }else{
        Foobar();
    }
}
