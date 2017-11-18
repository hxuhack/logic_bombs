#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include "a_tester.h"

void* Inc(void* i){
    int count = 0;
    while (*((int *) i) > -1000 && count++ < 1000){
	++ *((int *) i);
        //printf("%d\n", *((int*) i));
    }
}

void* Dec(void* i){
    int count = 0;
    while (*((int *) i) <  1000 && count++ < 1000){
	-- *((int *) i);
        //printf("%d\n", *((int *) i));
    }
}

int ThreadProp(int in){
    pthread_t tid[2];
    pthread_create(&tid[0], NULL, Inc, (void *) &in); 
    pthread_create(&tid[1], NULL, Dec, (void *) &in); 
    pthread_join(tid[0], NULL); 
    pthread_join(tid[1], NULL); 
    return in;
}

// {"s":{"length": 4}}
int logic_bomb(char* s) {
    int symvar = s[0] - 48;
    int i=ThreadProp(symvar-909);
    //printf("%d\n",i);
    if(i == -1900)
        return  BOMB_ENDING;
    return  NORMAL_ENDING;
}
