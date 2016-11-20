/*
Solution: 1.0000001
*/
#include<stdio.h>
#include"utils.h"

int main(int argc, char** argv){
    float x = atof(argv[1]);
    if(1 + x == 2 && x != 1){
       	Bomb();
     }
    else
	Foobar();
}
