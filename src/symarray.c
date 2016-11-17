/*
*solution: argv[1] = 0.00001
*/
#include<stdio.h>
#include"utils.h"

int main(int argc, char** argv){
    int ary[] ={1,2,3,4,5}; 
    int x = atoi(argv[1]);
    if(ary[x] == 5){
       	Bomb();
     }
    else
	Foobar();
}
