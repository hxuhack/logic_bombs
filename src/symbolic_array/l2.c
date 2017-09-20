/*
*solution: 
*/
#include<stdio.h>
#include"utils.h"

int main(int argc, char** argv){
    int l1_ary[] ={1,2,3,4,5}; 
    int l2_ary[] ={6,7,8,9,10}; 

    int x = atoi(argv[1]);
    if(l2_ary[l1_ary[x]] == 9){
       	Bomb();
     }
    else
	Foobar();
}
