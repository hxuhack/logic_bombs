/*
*Read CPU info as symbolic variables, if the CPU is not Intel,the bomb would be triggered.
*Evaluation:
--Triton: fail
--Angr:
--BAP:
*/
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include "a_tester.h"

int logic_bomb() {
   FILE *cpuinfo = fopen("/proc/cpuinfo", "rb");
   char *arg = 0;
   size_t size = 0;
   int trigger = 1;
   while(getdelim(&arg, &size, 0, cpuinfo) != -1)
   {
      if(strstr(arg,"Intel")){
	  trigger = 0;
      }
      puts(arg);
    
   }
   free(arg);
   fclose(cpuinfo);

   if(trigger)
    return BOMB_ENDING;
   else
    return NORMAL_ENDING;
}
