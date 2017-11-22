#include <unistd.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <sys/stat.h>
#include <sys/types.h>
#include "utils.h"
#include "a_tester.h"

// {"s":{"length": 2}}
int logic_bomb(char* symvar) {
    char *p_addr, *c_addr;
    int flag = 0;
    key_t shmid = shmget(IPC_PRIVATE, 1024, S_IRUSR|S_IWUSR);
    if (shmid < 0)
	return NORMAL_ENDING;
    pid_t pid = fork();
    if(pid == 0){
	p_addr = shmat(shmid,0,0);
        memset(p_addr,'/0',1024);
        strncpy(p_addr, symvar, 1024);
	exit(0);
    }
    if (pid > 0){
	sleep(1);
        c_addr = shmat(shmid,0,0);
        if(strcmp(c_addr, "7") == 0)
	    flag = 1;
        shmctl(shmid,IPC_RMID,0);
        if(flag == 1)
	    return BOMB_ENDING;
	return NORMAL_ENDING;
    }
}
