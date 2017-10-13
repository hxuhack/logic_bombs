#include <iostream>
#include "utils.h"

using namespace std;

double division(int numerator, int denominator) {
   if( denominator == 0 ) {
      throw "Division by zero condition!";
   }
   return (numerator/denominator);
}

#include "a_tester.h"


int sym_checker(int i) {
   int num = 10;

   try {
      division(num, i);
      return NORMAL_ENDING;
   }catch (const char* msg) {
      cerr << msg << endl;
      return BOMB_ENDING;
   }
}
