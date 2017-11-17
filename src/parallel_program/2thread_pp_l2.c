#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include "a_tester.h"

void* Inc(void* i){
    int count = 0;
    while (*((int *) i) > -500 && count++ < 1000){
	++ *((int*) i);
    }
}

void* Dec(void* i){
    int count = 0;
    while (*((int *) i) < 500 && count++ < 1000){
	-- *((int*) i);
    }
}

int ThreadProp(int in){
    pthread_t tid[2];
    int rc1 = pthread_create(&tid[0], NULL, Inc, (void *) &in); 
    int rc2 = pthread_create(&tid[1], NULL, Dec, (void *) &in); 
    rc1 = pthread_join(tid[0], NULL); 
    rc2 = pthread_join(tid[1], NULL); 
    return in;
}

int logic_bomb(int symvar) {
    int i=ThreadProp(symvar) % 10;
    if(i == 7)
        return  BOMB_ENDING;
    return  NORMAL_ENDING;
}
