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

int open_socket(char* host,char *port){
    struct addrinfo *res;//<netdb.h>
    struct addrinfo hints;
    memset(&hints,0,sizeof(hints));
    hints.ai_family=PF_UNSPEC;
    hints.ai_socktype=SOCK_STREAM;
    if(getaddrinfo(host,port,&hints,&res)==-1)
	return -1;
    int sock=socket(res->ai_family,res->ai_socktype, res->ai_protocol);
    if(sock==-1)
	return -1;

    int con=connect(sock,res->ai_addr,res->ai_addrlen);
    freeaddrinfo(res);
    if(con==-1)
	return -1;
    return sock;
}
