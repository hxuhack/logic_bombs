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

char* shell(const char* cmd)
{
    char* rs = "";
    FILE *f;
    f = popen(cmd, "r");
    char buf[1024];
    memset(buf,'\0',sizeof(buf));
    while(fgets(buf,1024-1,f)!=NULL)
    { 
       rs = buf;
    }

    pclose(f);
    return rs;
}

int logic_bomb() {
   char cmd[] = "ls -l |grep '^-'|wc -l";
   char* rs = shell(cmd);
   if(atoi(rs) == 7)
    return BOMB_ENDING;
   else
    return NORMAL_ENDING;
}
