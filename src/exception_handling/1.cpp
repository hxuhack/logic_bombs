#include <iostream>
#include "utils.h"

using namespace std;

double toy(int num) {
   if( num == 0 ) {
      throw "zero condition!";
   }
   return (num++);
}



#include "a_tester.h"


int logic_bomb(int i) {
   try {
      toy(i);
      return NORMAL_ENDING;
   }catch (const char* msg) {
      cerr << msg << endl;
      return BOMB_ENDING;
   }
}
