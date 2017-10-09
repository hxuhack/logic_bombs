/*
TOY:
*/
#include <string.h> 
#include "utils.h"

#include "a_tester.h"

int sym_checker(int i) {

    int trigger = 0; 
    FILE *fp = fopen(argv[1], "r");
    if(fp != NULL)
    {
	trigger = 1;
        fclose(fp);
    }

    if(trigger){
        return BOMB_ENDING;
    } else{
        return NORMAL_ENDING;
    }
}
