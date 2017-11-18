#include<stdio.h>
#include"utils.h"
#include "a_tester.h"

// {"s":{"length": 4}}
int logic_bomb(char* s) {
    int symvar = s[0] - 48;
    int ary[] ={1,2,3,4,5};
    if(ary[symvar%5] == 5){
        return BOMB_ENDING;
     }
    else
	return NORMAL_ENDING;
}
