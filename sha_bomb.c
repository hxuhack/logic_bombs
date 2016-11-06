/*
TOY:
*/
#include <stdio.h>
#include <sys/time.h>
#include "klee/klee.h"
#include "sha1.h"

void F0(int i){
    printf("%d\n", i);
}
void F1(int i){
    printf("%d\n", --i);
}
void F2(int i){
    printf("%d\n", ++i);
}
void F3(int i){
    printf("%d\n", i++);
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

int main(){
    int v1;
    klee_make_symbolic(&v1, sizeof(v1), "v1");
    printf("v1:%d\n",v1);
    unsigned cipher[5];
    cipher[0] = 0X77de68da;
    cipher[1] = 0Xecd823ba;
    cipher[2] = 0Xbbb58edb;
    cipher[3] = 0X1c8e14d7;
    cipher[4] = 0X106e83bb;

    while(SHA1_COMP(v1,cipher)){
      if (v1==0||v1==100){
        F0(v1);
        v1++;
      }else{
        v1+=2;
      }
    }
}
