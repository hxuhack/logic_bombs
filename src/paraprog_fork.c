/*
TOY:
*/
#include "utils.h"

int main(int argc, char** argv){
    int pid;
    int i=atoi(argv[1]);

    if((pid=fork())==-1)
	return -1;
    if(pid == 0){
        i++;
    }
    
    else{
        if(i==2){
            Bomb();
        }
        Foobar();
    }
}
