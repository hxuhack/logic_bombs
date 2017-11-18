/*
TOY:
*/
#include <string.h> 
#include "utils.h"

#include "a_tester.h"

int df2cf(char a)
{
    int b;
    switch(a){
      case 0:
        b = 0;
	break;
      case 1:
        b = 1;
	break;
      case 2:
        b = 2;
	break;
      case 3:
        b = 3;
	break;
      case 4:
        b = 4;
	break;
      case 5:
        b = 5;
	break;
      case 6:
        b = 6;
	break;
      case 7:
        b = 7;
	break;
      case 8:
        b = 8;
	break;
      case 9:
        b = 9;
	break;
      default:
        b = 0;
        break;
    }
    return b;
}

// {"s":{"length": 4}}
int logic_bomb(char* s) {
    int symvar = s[0] - 48;
    int a = df2cf(symvar%10);
    a++;
    int b = symvar + a;
    if(b == 15)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
