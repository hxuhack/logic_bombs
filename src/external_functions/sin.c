/*
TOY:
Solution: 30
*/
#include <string.h> 
#include "utils.h"

#define PI 3.14159265358979323846264338327

int main(int argc, char** argv){
    int i = atoi(argv[1]);
    float v = sin(i*PI/180);
    if(v == 0.5){
        Bomb();
    }else{
        Foobar();
    }
}
