/*
TOY:
*/
#include <string.h> 
#include "utils.h"

int main(int argc, char** argv){

    int j,i=atoi(argv[1]); 
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
    if(j == 7){
        Bomb();
    } else{
        Foobar();
    }
    remove(file);
}
