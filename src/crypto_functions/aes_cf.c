/*
TOY:
* Solution: 2b7e151628aed2a6abf7158809cf4f3c
*/
#include <inttypes.h>
#include "aes.h"
#include "utils.h"

void aes_print(uint8_t* str) {
    unsigned char i;
    for(i = 0; i < 16; ++i)
        printf("%.2x", str[i]);
    printf("\n");
}

#include "a_tester.h"

// {"s":{"length": 32}}
int logic_bomb(char* s) {
    if(strlen(s) != 32){
        //printf("please input the 128-bit keys\n");
	return NORMAL_ENDING;
    }

    uint8_t key[16];

    sscanf(s,
        "%2" SCNx8 "%2" SCNx8
        "%2" SCNx8 "%2" SCNx8
        "%2" SCNx8 "%2" SCNx8
        "%2" SCNx8 "%2" SCNx8
    	"%2" SCNx8 "%2" SCNx8
    	"%2" SCNx8 "%2" SCNx8
   	"%2" SCNx8 "%2" SCNx8
    	"%2" SCNx8 "%2" SCNx8,
    	&key[0],&key[1],
    	&key[2],&key[3],
    	&key[4],&key[5],
    	&key[6],&key[7],
    	&key[8],&key[9],
    	&key[10],&key[11],
    	&key[12],&key[13],
    	&key[14],&key[15]);

    //aes_print(key);

    uint8_t decodetext[16];
    uint8_t ciphertext[] = {0x3a, 0xd7, 0x7b, 0xb4, 0x0d, 0x7a, 0x36, 0x60, 0xa8, 0x9e, 0xca, 0xf3, 0x24, 0x66, 0xef, 0x97};
    uint8_t plaintext[] = {0x6b, 0xc1, 0xbe, 0xe2, 0x2e, 0x40, 0x9f, 0x96, 0xe9, 0x3d, 0x7e, 0x11, 0x73, 0x93, 0x17, 0x2a};

    AES128_ECB_decrypt(ciphertext, key, decodetext);

    //aes_print(decodetext);
    if(0 == memcmp((char*) plaintext, (char*) decodetext, 16)){
        return BOMB_ENDING;
    }else{
        return NORMAL_ENDING;
    }
}
