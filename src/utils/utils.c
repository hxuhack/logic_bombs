/*
TOY:
*/
#include "utils.h"
#include "sha1.h"

void Bomb(){
    printf("bomb triggered\n");
}
void Foobar(){
    printf("nomal execution\n");
}
int GetSec(){
    time_t t_t;
    struct tm* t_tm;
    time(&t_t);
    t_tm = gmtime(&t_t);
    int sec = (int) t_tm->tm_sec;
    printf("Current second: %d\n", sec);
    return sec;
}

long GetSecSince1970(){
    struct timeval tv;
    gettimeofday(&tv, NULL);
    printf("Seconds sine 1970: %ld\n", tv.tv_sec);
    return tv.tv_sec;
}

int SHA1_COMP(int plaintext, unsigned ciphertext[5])
{
    SHA1Context sha;
    char* input;
    int i;

    input = (char *) malloc (sizeof(char)*33);
    sprintf(input, "%d", plaintext);
    printf("plaintext = %d\n", plaintext);
    SHA1Reset(&sha);
    SHA1Input(&sha, (const unsigned char *) input, strlen(input));

    if (!SHA1Result(&sha))
    {
        fprintf(stderr, "ERROR-- could not compute message digest\n");
        return -1;
    }
    for(i = 0; i < 5 ; i++)
    {
        if(ciphertext[i]!=sha.Message_Digest[i])
            return 1;
    }
    return 0;
}
