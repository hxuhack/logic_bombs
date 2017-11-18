#include <iostream>
#include <list>
#include <vector>
#include "utils.h"
#include "a_tester.h"

using namespace std;

// {"s":{"length": 4}}
int logic_bomb(char* s) {
    int symvar = s[0] - 48;
    list<int> mylist;
    for (int i=0; i<10; i++){
	mylist.push_back(i);
    }
    list<int>::iterator it = mylist.begin();
    advance(it, symvar%10);
    if(*it == 7)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
