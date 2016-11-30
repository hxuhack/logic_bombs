/*
TOY:
*/
#include <unistd.h> 
#include "utils.h"

int main(int argc, char** argv){
    int pid, fd[2];
    pipe(fd);
    if((pid=fork())==-1)
	return -1;
    if(pid == 0){
        close(fd[0]);
        write(fd[1],argv[1],sizeof(argv[1]));
	wait(NULL);
    }
    else{
	char content[8];
        close(fd[1]);
        read(fd[0],content,8);
        if(strcmp(content,"7")==0){
            Bomb();
        }else{
            Foobar();
        }
    }
}
