/*
   TOY:
 */
#include <unistd.h>
#include "utils.h"

#include "a_tester.h"

// {"s":{"length": 16}}
int logic_bomb(char* s) {
    int pid, fd[2];
    pipe(fd);
    if ((pid = fork()) == -1)
        return -1;
    if (pid == 0) {
        close(fd[0]);
        write(fd[1], s, sizeof(s));
        wait(NULL);
    }
    else {
        char content[8];
        close(fd[1]);
        read(fd[0], content, 8);
        if (strcmp(content, "7") == 0) {
            Bomb();
        }
        else {
            Foobar();
        }
    }
}
