/*
TOY:
*/
#include <string.h> 
#include "utils.h"

int main(int argc, char** argv){

    int trigger = 0; 
    trigger=system(argv[1]);

    printf ("%d\n", trigger);
    if(trigger == 0){
        Bomb();
    } else{
        Foobar();
    }
}
