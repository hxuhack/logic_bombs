#include <fstream>
#include <iostream>
#include <stdexcept>
#include "utils.h" 

using namespace std;

#include "a_tester.h"


int sym_checker(int i) {
    ifstream file;
    file.exceptions ( ifstream::failbit | ifstream::badbit );
    try {
        file.open (argv[1]);
        file.close();
        return NORMAL_ENDING;
    }
    catch (const ifstream::failure& e) {
        cout << "Exception opening/reading file:" <<e.what()<<"\n";
	if (strstr(e.what(), "basic_ios::clear"))
        return BOMB_ENDING;
    }
    return NORMAL_ENDING;
}
