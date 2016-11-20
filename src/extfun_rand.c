/*
TOY:
Solution: 7
*/
#include <string.h> 
#include "utils.h"

int main(int argc, char** argv){
    srand(atoi(argv[1]));
    int r = rand()%100;
    if(r == 77){
        Bomb();
    }else{
        Foobar();
    }
}
