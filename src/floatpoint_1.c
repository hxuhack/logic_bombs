/*
*solution: argv[1] = 0.00001
*/
#include<stdio.h>
#include"utils.h"

int main(int argc, char** argv){
    float x = atof(argv[1]);
    if(1024+x==1024 && x>0){
       	Bomb();
     }
    else
	Foobar();
}
