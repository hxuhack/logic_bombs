#include <fstream>
#include <iostream>
#include <stdexcept>
#include "utils.h"

using namespace std;

#include "a_tester.h"

// {"s":{"length": 32}}
int logic_bomb(char* s) {
     if(s == NULL)
	return NORMAL_ENDING;
    if(s[0]=='\0')
        return NORMAL_ENDING;
    ifstream file;
    file.exceptions ( ifstream::failbit | ifstream::badbit);
    try {
        file.open(s);
        file.close();
        return BOMB_ENDING;
    }
    catch (const ifstream::failure& e) {
        //cout << "Exception opening/reading file:" <<e.what()<<"\n";
	//if (strstr(e.what(), "basic_ios::clear"))
        return NORMAL_ENDING;
    }
    return NORMAL_ENDING;
}
