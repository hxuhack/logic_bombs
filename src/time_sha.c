/*
TOY:
*/
#include "sha1.h"
#include "utils.h"

int main(int argc, char** argv){
    long plaintext = GetSecSince1970();

    unsigned cipher[5];
    cipher[0] = 0X1743582b;
    cipher[1] = 0X5b60c87f;
    cipher[2] = 0X326b31cb;
    cipher[3] = 0X8795d908;
    cipher[4] = 0Xece3a097;

    if(SHA1_COMP(plaintext,cipher)==0){
        Bomb();
    }else{
        Foobar();
    }
}
