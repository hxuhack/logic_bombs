/*
TOY:
*/
#include "sha1.h"
#include "utils.h"

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
