#include <iostream>
#include "utils.h"

using namespace std;

double toy(int num) {
   if( num == 0 ) {
      throw "zero condition!";
   }
   return (num++);
}

int main (int argc, char** argv) {
   if (argc != 2)
	return -1;

   int i = atoi(argv[1]);
 
   try {
      toy(i);
      Foobar();
   }catch (const char* msg) {
      cerr << msg << endl;
      Bomb();
   }

   return 0;
}
