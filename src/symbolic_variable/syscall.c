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

int main(int argc, char **argv)
{
   int trigger;
   char cmd[] = "dir";
   trigger=system (cmd);
   printf ("The value returned was: %d.\n",trigger);
   if(trigger)
	Bomb();
   else
	Foobar();
   return 0;
}
