/*
* Bomb type: system call
* Info: This bomb checks if a program has been uninstalled.
* If the command cannot be executed, the bomb will be triggered.
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
