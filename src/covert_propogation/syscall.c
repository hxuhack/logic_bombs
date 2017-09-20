/*
TOY:
*/
#include <string.h> 
#include "utils.h"

int main(int argc, char** argv){

    int j,i=atoi(argv[1]); 
    char file[] = "tmp.covpro";
    char cmd[256];
    sprintf(cmd, "echo %d > %s\n", i, file); 
    system(cmd);

    FILE *fp = stdin;
    fp = fopen(file, "r");
    fscanf(fp,"%d",&j);
    fclose(fp);

    if(j == 7){
        Bomb();
    } else{
        Foobar();
    }

    remove(file);
}
