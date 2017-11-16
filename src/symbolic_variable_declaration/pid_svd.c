#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "a_tester.h"

int logic_bomb() {
   int pid = (int) getpid();
   if(pid == 4096)
    return BOMB_ENDING;
   else
    return NORMAL_ENDING;
}
