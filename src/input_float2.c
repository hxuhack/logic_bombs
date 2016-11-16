#include<stdio.h>
#include"utils.h"

int main(int argc, char** argv){
    float x = atof(argv[1]);
    if(0.5 + x== 1 && x != 0.5){
       	Bomb();
     }
    else
	Foobar();
}
