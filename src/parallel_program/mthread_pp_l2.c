#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include "a_tester.h"

void* Inc(void* i){
    int count = 0;
    while (*((int *) i) > -1000 && count++ < 1000){
	++ *((int*) i);
    }
}

void* Dec(void* i){
    int count = 0;
    while (*((int *) i) < 1000 && count++ < 1000){
	-- *((int*) i);
    }
}

int ThreadProp(int in){
    pthread_t tid[10];
    pthread_create(&tid[0], NULL, Inc, (void *) &in); 
    pthread_create(&tid[1], NULL, Dec, (void *) &in); 
    pthread_create(&tid[2], NULL, Inc, (void *) &in); 
    pthread_create(&tid[3], NULL, Dec, (void *) &in); 
    pthread_create(&tid[4], NULL, Inc, (void *) &in); 
    pthread_create(&tid[5], NULL, Dec, (void *) &in); 
    pthread_create(&tid[6], NULL, Inc, (void *) &in); 
    pthread_create(&tid[7], NULL, Dec, (void *) &in); 
    pthread_create(&tid[8], NULL, Inc, (void *) &in); 
    pthread_create(&tid[9], NULL, Dec, (void *) &in); 
    pthread_join(tid[0], NULL); 
    pthread_join(tid[1], NULL); 
    pthread_join(tid[2], NULL); 
    pthread_join(tid[3], NULL); 
    pthread_join(tid[4], NULL); 
    pthread_join(tid[5], NULL); 
    pthread_join(tid[6], NULL); 
    pthread_join(tid[7], NULL); 
    pthread_join(tid[8], NULL); 
    pthread_join(tid[9], NULL); 
    return in;
}

int logic_bomb(int symvar) {
    int i=ThreadProp(symvar+990);
    //printf("%d\n",i);
    if(i == 5999)
        return  BOMB_ENDING;
    return  NORMAL_ENDING;
}
