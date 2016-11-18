/*
TOY:
*/
#include <pthread.h> 
#include "utils.h"

void* Inc(void* i){
    ++ *((int*) i);
}
int main(int argc, char** argv){
    pthread_t thread;
    int i = atoi(argv[1]);
    int rc = pthread_create(&thread, NULL, Inc, (void *) &i); 

    rc = pthread_join(thread, NULL); 
    if(i == 7){
        Bomb();
    }
    Foobar();
}
