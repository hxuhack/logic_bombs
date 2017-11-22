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


// {"s":{"length": 4}}
int logic_bomb(char* s) {
    int symvar = s[0] - 48;
    try {
       toy(symvar);
       return NORMAL_ENDING;
    }catch (const char* msg) {
       return BOMB_ENDING;
    }
}
