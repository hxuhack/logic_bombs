#include <fstream>
#include <iostream>
#include <stdexcept>
#include "utils.h" 

using namespace std;

int main (int argc, char** argv) 
{
    if(argc < 2){
	return -1;
    }
    ifstream file;
    file.exceptions ( ifstream::failbit | ifstream::badbit );
    try {
        file.open (argv[1]);
        Foobar(); 
        file.close();
    }
    catch (const ifstream::failure& e) {
        cout << "Exception opening/reading file:" <<e.what()<<"\n";
	if (strstr(e.what(), "basic_ios::clear"))
	    Bomb();	
    }

    return 0;
}
