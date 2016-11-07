#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

int main(int argc, char **argv)
{
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
	Bomb();
   else
	Foobar();
   return 0;
}
