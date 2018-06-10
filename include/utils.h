/*
TOY:
*/
#ifndef _BOMB_UTILS_H_
#define _BOMB_UTILS_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <err.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <stdarg.h>

#ifdef __cplusplus
extern "C" {
#endif

void Bomb();

void Foobar();

int GetSec();

long GetSecSince1970();

int SHA1_COMP(int, unsigned[5]);

int open_socket(char* host,char *port);

#ifdef __cplusplus
}
#endif
#endif
