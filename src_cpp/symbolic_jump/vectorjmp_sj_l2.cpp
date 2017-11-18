#include <iostream>
#include <vector>
#include "utils.h"
#include "a_tester.h"

using namespace std;

#define jmp(addr) asm("jmp *%0"::"r"(addr):)

// {"s":{"length": 4}}
int logic_bomb(char* s) {
    int symvar = s[0] - 48;
    vector<int> myvector;
    myvector.push_back(7);
    myvector.push_back(13);
    myvector.push_back(14);
    myvector.push_back(15);
    myvector.push_back(16);
    myvector.push_back(21);
    myvector.push_back(22);
    myvector.push_back(37);
    myvector.push_back(23);
    myvector.push_back(24);

    long long addr = (long long) &&flag_0 + myvector.at(symvar%10);
    jmp(addr);
  flag_0:
    if (symvar > 0){
        symvar++;
        if(symvar == 0)
            return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
