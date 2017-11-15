#include<stdio.h>
#include<stdlib.h>
#include"utils.h"
#include "a_tester.h"

int logic_bomb(int i) {
    int *array = (int *) malloc(sizeof(int) * 10);
    int k = 0;
    for (k=0; k<10; k++){
	array[k] = k;
    }
    if(array[i%10] == 7){
       return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
