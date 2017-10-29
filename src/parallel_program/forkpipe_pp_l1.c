#include <unistd.h>
#include "utils.h"
#include "a_tester.h"

int logic_bomb(char* s) {
    int pid, fd[2];
    pipe(fd);
    if ((pid = fork()) == -1)
        return NORMAL_ENDING;
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
            return BOMB_ENDING;
        }
        return NORMAL_ENDING; 
    }
}
