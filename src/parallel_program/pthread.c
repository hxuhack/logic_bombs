/*
TOY:
*/
#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include "a_tester.h"

void* inc(void* i) {
    long long* j = (long long*)i;
    unsigned long start = (unsigned long)time(NULL);

    while ((unsigned long)time(NULL) - start < 2)
        *j += 1;
}

void* dec(void* i) {
    long long* j = (long long*)i;
    unsigned long start = (unsigned long)time(NULL);

    while ((unsigned long)time(NULL) - start < 2)
        *j -= 1;
}

int sym_checker(long long* i) {
    pthread_t thread1, thread2;
    int rc1 = pthread_create(&thread1, NULL, inc, (void*)i);
    int rc2 = pthread_create(&thread2, NULL, dec, (void*)i);
    int flag;

    sleep(1);

    if (*i > 0)
        flag = BOMB_ENDING;
    else
        flag = NORMAL_ENDING;

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    return flag;
}
