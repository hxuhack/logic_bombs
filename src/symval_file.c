/*
TOY:
*/
#include <string.h> 
#include "utils.h"

int main(int argc, char** argv){

    int trigger = 0; 
    FILE *fp = fopen(argv[1], "r");
    if(fp != NULL)
    {
	trigger = 1;
        fclose(fp);
    }

    if(trigger){
        Bomb();
    } else{
        Foobar();
    }
}
