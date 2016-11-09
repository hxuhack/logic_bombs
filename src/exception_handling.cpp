#include <iostream>
#include "utils.h"

using namespace std;

double division(int a, int b) {
   if( b == 0 ) {
      throw "Division by zero condition!";
   }
   return (a/b);
}

int main (int argc, char** argv) {
   if (argc != 3)
	return -1;

   int x = atoi(argv[1]);
   int y = atoi(argv[2]);

   double z = 0;
 
   try {
      z = division(x, y);
      Foobar();
      cout << z << endl;
   }catch (const char* msg) {
      cerr << msg << endl;
      Bomb();
   }

   return 0;
}
