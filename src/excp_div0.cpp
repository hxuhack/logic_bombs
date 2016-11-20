#include <iostream>
#include "utils.h"

using namespace std;

double division(int numerator, int denominator) {
   if( denominator == 0 ) {
      throw "Division by zero condition!";
   }
   return (numerator/denominator);
}

int main (int argc, char** argv) {
   if (argc != 2)
	return -1;

   int num = 10;
   int denom = atoi(argv[1]);

 
   try {
      division(num, denom);
      Foobar();
   }catch (const char* msg) {
      cerr << msg << endl;
      Bomb();
   }

   return 0;
}
