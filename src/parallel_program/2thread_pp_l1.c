#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include "a_tester.h"

void* Inc(void* i){
	++ *((int*) i);
}

void* Mult(void* i){
	*((int*) i) =  *((int*) i) * *((int*) i);
}

int ThreadProp(int in){
	pthread_t tid[2];
	int rc1 = pthread_create(&tid[0], NULL, Inc, (void *) &in); 
	int rc2 = pthread_create(&tid[1], NULL, Mult, (void *) &in); 
	rc1 = pthread_join(tid[0], NULL); 
	rc2 = pthread_join(tid[1], NULL); 
	int out = in;
	return out;
}

int logic_bomb(int symvar) {
    int i=ThreadProp(symvar);
    printf ("%d\n", i);
    if(i == 50)
        return  BOMB_ENDING;
    return  NORMAL_ENDING;
}
