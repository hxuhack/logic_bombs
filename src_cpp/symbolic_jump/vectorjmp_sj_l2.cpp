#include <iostream>
#include <vector>
#include "utils.h"
#include "a_tester.h"

using namespace std;

#define jmp(addr) asm("jmp *%0"::"r"(addr):)

int logic_bomb(int symvar) {
    vector<int> myvector;
    myvector.push_back(0);
    myvector.push_back(4);
    myvector.push_back(4);
    myvector.push_back(0);
    myvector.push_back(21);
    myvector.push_back(16);
    myvector.push_back(21);

    int idx = symvar%myvector.size();
    printf("idx:ele = %d:%d, \n", idx,myvector.at(idx));
    long long addr = (long long) &&flag_0 + myvector.at(idx);
    printf("addr = %x, \n", addr);
    jmp(addr);
  flag_0:
    if (symvar > 0){
        symvar++;
        if(symvar == 0)
            return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
