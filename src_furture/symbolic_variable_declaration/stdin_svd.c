#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>

#include "a_tester.h"

int logic_bomb() {
   int symvar;
   scanf("%d", &symvar);
   if(symvar == 7)
    return BOMB_ENDING;
   else
    return NORMAL_ENDING;
}
