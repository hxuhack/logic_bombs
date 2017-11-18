#include <iostream>
#include "utils.h"

using namespace std;

double toy(int num) {
   if( num == 7 ) {
      throw "zero condition!";
   }
   return (num++);
}



#include "a_tester.h"


int logic_bomb(int symvar) {
   try {
      toy(symvar);
      return NORMAL_ENDING;
   }catch (const char* msg) {
      return BOMB_ENDING;
   }
}
