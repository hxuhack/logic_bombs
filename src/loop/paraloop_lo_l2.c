#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include "a_tester.h"

void* trigger(void* i){
    sleep(5);
    ++ *((int*) i);
}

int logic_bomb(int symvar) {
    int i = symvar + 1;
    pthread_t tid;
    int rc = pthread_create(&tid, NULL, trigger, (void *) &symvar); 
    while (symvar != i){
	sleep(1);
        symvar ++;
        i ++;
    }
    rc = pthread_join(tid, NULL); 
    printf("symvar = %d\n", symvar);
    if(symvar == 13)
        return  BOMB_ENDING;
    return  NORMAL_ENDING;
}