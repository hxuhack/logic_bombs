#include <iostream>
#include <list>
#include <vector>
#include "utils.h"
#include "a_tester.h"

using namespace std;

int logic_bomb(int symvar) {
    list<int> mylist;
    for (int i=0; i<10; i++){
	mylist.push_back(i);
    }
    list<int>::iterator it = mylist.begin();
    advance(it, symvar);
    if(*it == 7)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
