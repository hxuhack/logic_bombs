#include<stdio.h>
#include"utils.h"
#include "a_tester.h"

int logic_bomb(int i) {
    int ary[] ={1,2,3,4,5};
    if(ary[i] == 5){
        return BOMB_ENDING;
     }
    else
	    return NORMAL_ENDING;
}
