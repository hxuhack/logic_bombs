#include <iostream>
#include <vector>
#include "utils.h"
#include "a_tester.h"

using namespace std;

int logic_bomb(int symvar) {
    vector<int> myvector;
    for (int i=0; i<10; i++){
	myvector.push_back(i);
    }
    if(myvector.at(symvar) == 7)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
