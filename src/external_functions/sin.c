/*
TOY:
Solution: 30
*/
#include <string.h> 
#include <math.h>
#include "utils.h"

#define PI 3.14159265358979323846264338327

#include "a_tester.h"

int logic_bomb(int i) {
    float v = sin(i*PI/180);
    if(v == 0.5){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
