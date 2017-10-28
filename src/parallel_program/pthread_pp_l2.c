#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include "a_tester.h"

void* Inc(void* i){
    int count = 0;
    while (*((int *) i) > -500 && count++ < 1000){
	++ *((int*) i);
        printf("%d\n", *((int*) i));
    }
}

void* Dec(void* i){
    int count = 0;
    while (*((int *) i) < 500 && count++ < 1000){
	-- *((int*) i);
        printf("%d\n", *((int*) i));
    }
}

int ThreadProp(int in){
    pthread_t thread;
    int rc1 = pthread_create(&thread, NULL, Inc, (void *) &in); 
    int rc2 = pthread_create(&thread, NULL, Dec, (void *) &in); 
    rc1 = pthread_join(thread, NULL); 
    rc2 = pthread_join(thread, NULL); 
    return in;
}

int logic_bomb(int symvar) {
    int i=ThreadProp(symvar);
    printf("i=%d\n",i);
    if(i == 10)
        return  BOMB_ENDING;
    return  NORMAL_ENDING;
}
