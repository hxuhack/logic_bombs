/*
*solution: 
*/
#include<stdio.h>
#include"utils.h"

#include "a_tester.h"

int sym_checker(int i) {
    int l1_ary[] ={1,2,3,4,5}; 
    int l2_ary[] ={6,7,8,9,10}; 

    int x = atoi(argv[1]);
    if(l2_ary[l1_ary[x]] == 9){
        return BOMB_ENDING;
     }
    else
        return NORMAL_ENDING;
}
