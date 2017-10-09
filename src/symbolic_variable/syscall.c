/*
* The bomb uses the result of syscall as symbolic variables. This bomb checks if a program has been uninstalled.  If the command cannot be executed, the bomb will be triggered.
*Evaluation:
--Triton: fail
--Angr:
--BAP:
*/
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

#include "a_tester.h"

int sym_checker() {
   int trigger;
   char cmd[] = "dir";
   trigger=system(cmd);
   printf("The value returned was: %d.\n",trigger);
   if(trigger)
    return BOMB_ENDING;
   else
    return BOMB_ENDING;
}
