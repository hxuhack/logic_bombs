/*
TOY:
Result:
Triton: Pin is out of memory: MmapChecked

*/
#include <string.h> 
#include "utils.h"
#include "a_tester.h"

int sym_checker(int i) {
    int j = i;
    char file[] = "tmp.covpro";
    FILE *fp = fopen(file, "ab+");
    if(fp == NULL)
    {
        printf("Error!");   
        exit(1);             
    }
    fprintf(fp,"%d",i);
    fclose(fp);

    fp = fopen("tmp.covpro", "r");
    fscanf(fp,"%d",&j);
    printf("i = %d, j = %d\n", i,j);   
    fclose(fp);
    remove(file);
    if(j == 7){
        return BOMB_ENDING;
    } else{
        return NORMAL_ENDING;
    }
}
