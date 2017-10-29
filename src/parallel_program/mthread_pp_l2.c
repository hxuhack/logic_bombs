#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include "a_tester.h"

void* Inc(void* i){
    int count = 0;
    while (*((int *) i) > -1000 && count++ < 1000){
	++ *((int*) i);
        printf("%d\n", *((int*) i));
    }
}

void* Dec(void* i){
    int count = 0;
    while (*((int *) i) < 1000 && count++ < 1000){
	-- *((int*) i);
        printf("%d\n", *((int*) i));
    }
}

int ThreadProp(int in){
    pthread_t tid[10];
    int rc1 = pthread_create(&tid[0], NULL, Inc, (void *) &in); 
    int rc2 = pthread_create(&tid[1], NULL, Dec, (void *) &in); 
    int rc3 = pthread_create(&tid[2], NULL, Inc, (void *) &in); 
    int rc4 = pthread_create(&tid[3], NULL, Dec, (void *) &in); 
    int rc5 = pthread_create(&tid[4], NULL, Inc, (void *) &in); 
    int rc6 = pthread_create(&tid[5], NULL, Dec, (void *) &in); 
    int rc7 = pthread_create(&tid[6], NULL, Inc, (void *) &in); 
    int rc8 = pthread_create(&tid[7], NULL, Dec, (void *) &in); 
    int rc9 = pthread_create(&tid[8], NULL, Inc, (void *) &in); 
    int rc10 = pthread_create(&tid[9], NULL, Dec, (void *) &in); 
    rc1 = pthread_join(tid[0], NULL); 
    rc2 = pthread_join(tid[1], NULL); 
    rc3 = pthread_join(tid[2], NULL); 
    rc4 = pthread_join(tid[3], NULL); 
    rc5 = pthread_join(tid[4], NULL); 
    rc6 = pthread_join(tid[5], NULL); 
    rc7 = pthread_join(tid[6], NULL); 
    rc8 = pthread_join(tid[7], NULL); 
    rc9 = pthread_join(tid[8], NULL); 
    rc10 = pthread_join(tid[9], NULL); 
    return in;
}

int logic_bomb(int symvar) {
    int i=ThreadProp(symvar);
    printf("i=%d\n",i);
    if(i == 502)
        return  BOMB_ENDING;
    return  NORMAL_ENDING;
}
