#include <fstream>
#include <iostream>
#include <stdexcept>
#include "utils.h" 

using namespace std;

int main (int argc, char** argv) 
{
    ifstream file;
    file.exceptions ( ifstream::failbit | ifstream::badbit );
    char filepath[] = "/home/hui/hostag.txt";
    try {
        file.open (filepath);
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
