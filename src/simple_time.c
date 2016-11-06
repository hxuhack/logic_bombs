#include <stdio.h>
#include <time.h>
#include <sys/time.h>

void F0(int i){
    printf("bomb triggered:%d\n", i);
}
void F1(int i){
    printf("nomal execution:%d\n", i);
}
int GetSec(){
    time_t t_t;
    struct tm* t_tm;
    time(&t_t);
    t_tm = gmtime(&t_t);
    printf("Current second: %d\n", t_tm->tm_sec);
    return t_tm->tm_sec;
}

int GetSecSince1970(){
    struct timeval tv;
    gettimeofday(&tv, NULL);
    printf("Seconds sine 1970: %ld\n", tv.tv_sec);
    return tv.tv_sec;
}

int main(){
    long v1 = GetSecSince1970();
    if(v1 > 2524608000 && v1< 2524608000 + 10){ //Jan 1st, 2050, 00:00::00
       F0(v1);
    }else{
       F1(v1);
    }
}
