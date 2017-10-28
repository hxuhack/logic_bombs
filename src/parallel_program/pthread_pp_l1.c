#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include "a_tester.h"

void* Inc(void* i){
	++ *((int*) i);
}

void* Dec(void* i){
	-- *((int*) i);
}

int ThreadProp(int in){
	pthread_t thread;
	int rc1 = pthread_create(&thread, NULL, Inc, (void *) &in); 
	int rc2 = pthread_create(&thread, NULL, Dec, (void *) &in); 
	rc1 = pthread_join(thread, NULL); 
	rc2 = pthread_join(thread, NULL); 
	int out = in;
	return out;
}

int logic_bomb(int symvar) {
    int i=ThreadProp(symvar);
    if (i!=symvar){
        if(i == 6)
        return  BOMB_ENDING;
    }
    return  NORMAL_ENDING;
}
