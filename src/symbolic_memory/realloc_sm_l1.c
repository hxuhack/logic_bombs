#include<stdio.h>
#include<stdlib.h>
#include"utils.h"
#include "a_tester.h"

int logic_bomb(int i) {
    int *array = (int *) malloc(sizeof(int) * 5);
    int k = 0;
    for (k=0; k<5; k++){
        array[k] = k;
    }
    array = (int *) realloc (array, sizeof(int) * 10);
    for (k=5; k<10; k++){
        array[k] = k;
    }
    if(array[i] == 7){
        return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}

