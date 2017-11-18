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


int logic_bomb(int symvar) {
   int num = 10;

   try {
      division(num, symvar-7);
      return NORMAL_ENDING;
   }catch (const char* msg) {
      return BOMB_ENDING;
   }
}
