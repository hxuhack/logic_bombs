/*
TOY:
*/
#include "sha1.h"
#include "utils.h"

int main(int argc, char** argv){
    int plaintext = atoi(argv[1]);
    unsigned cipher[5];
    cipher[0] = 0X77de68da;
    cipher[1] = 0Xecd823ba;
    cipher[2] = 0Xbbb58edb;
    cipher[3] = 0X1c8e14d7;
    cipher[4] = 0X106e83bb;

    if(SHA1_COMP(plaintext,cipher)==0){
        Bomb();
    }else{
        Foobar();
    }
}
